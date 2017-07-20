import re

class SVGParser:
    def __init__(self, fileData):
        self.data = fileData

    def evaluate(self):
        node = XMLNode(self.data)
        node.evaluate()
        self.result = self.generateResult(node.errors)

    def generateResult(self, errors):
        if len(errors) == 0:
            return ['SVG File Valid for Laser cutter']
        else:
            return ['SVG File Invalid. Errors:']+errors

class XMLNode:
    def __init__(self, raw_data):
        self.data = raw_data
        self.errors = []
        self.tags = []

    def evaluate(self):
        # Remove new lines from the svg file
        data = ' '.join(self.data.split('\n'))
        # Pull all of the XML tags from the SVG file
        tags = [a for a in re.findall('<.+?>', data) if not a.startswith('<?') and not a.startswith('<!')]
        # Generate an invalid file error
        if not tags and data:
            self.errors.append('Invalid SVG File')
            return

        # Pull the tag types out of the tags
        tag_types = [a[1:-1].split()[0] for a in tags]
        opening = None
        # Iterate all of the tags
        for i, tag in enumerate(tag_types):
            if opening == None and not tag.startswith('/'):
                # open the tag and begin recording data
                opening = tag
            if opening and (tag == '/'+opening or tags[tag_types.index(opening)].endswith('/>')):
                inner_text = ''
                if tag != opening:
                    # Close the tag and pull all of the data in
                    inner_text = ''.join(tags[tag_types.index(opening)+1:i])
                # If its a closing tag, then clip the tag type
                if tag.startswith('/'):
                    tag = tag[1:]
                # Add a top-level tag to the tag list
                self.tags.append(TagNode(tag, self.getAttributes(tags[tag_types.index(opening)]), inner_text))
                opening = None
        # Iterate and parse each tag
        for tag in self.tags:
            tag.evaluate()
            self.errors += tag.errors

    def getAttributes(self, tag):
        tag = tag[1:-1]
        attrs = re.findall(r'[^ \t]+?="[^ \t]+?"', tag)
        attr_dict = {}
        for a in attrs:
            a = a.strip().split('=')
            attr_dict[a[0]] = a[1][1:-1]
        return attr_dict

class TagNode:
    def __init__(self, tag_type, attrs, inner_text):
        self.attributes = attrs
        self.tag_type = tag_type
        self.inner_text = inner_text
        self.errors = []

    def __str__(self):
        return 'Tag(type={}, inner_text="{}", attributes="{}")'.format(self.tag_type, self.inner_text, self.attributes)

    def evaluate(self):
        if self.inner_text:
            node = XMLNode(self.inner_text)
            node.evaluate()
            self.errors = node.errors
        for a in self.attributes:
            if a != "style":
                self.checkAttribute(a, self.attributes[a])
            # Split the style up and parse those
            elif a == "style":
                styles = self.attributes[a].split(';')
                for style in styles:
                    style = style.split(':')
                    self.checkAttribute(*style)

    def checkAttribute(self, a, val):
        val = val.lower()
        # find an invalid stroke colour attribute
        if a == "stroke":
            if val.lower() not in ('red', 'rgb(255, 0, 0)', '#ff0000', 'blue', 'rgb(0, 0, 255)', '#0000ff', "none"):
                self.errors.append('Stroke colour is not RGB Red or RGB Blue on {} object'.format(self.tag_type))
        # Find an invalid fill colour attribute
        elif a == "fill":
            if val.lower() not in ('black', 'rgb(0, 0, 0)', "#000000", "none"):
                self.errors.append('Fill colour is not Black in {} object'.format(self.tag_type))
        # Find an invalid stroke width attribute
        elif a == "stroke-width":
            if eval(val) != 0.001:
                self.errors.append('Incorrect stroke width in {} object'.format(self.tag_type))
