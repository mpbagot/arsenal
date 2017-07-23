import re

class SVGParser:
    def __init__(self, fileData):
        self.data = fileData
        self.width = 0
        self.style = {}

    def evaluate(self):
        # Protect the CSS by placing it into a tag
        self.data = self.data.replace('<style>', '<style><')
        self.data = self.data.replace('</style>', '></style>')
        node = XMLNode(self, self.data)
        node.evaluate()
        self.width = node.width
        self.result = self.generateResult(node.errors)

    def getStylesFor(self, tag_type, attrs):
        tag_class = attrs.get('class')
        tag_id = attrs.get(id)
        styles = []
        if tag_id:
            styles += self.style.get('#'+tag_id, '').split(';')
        if tag_class:
            styles += self.style.get('.'+tag_class, '').split(';')
        styles += self.style.get(tag_type, '').split(';')
        return [a for a in styles if a]

    def generateResult(self, errors):
        if len(errors) == 0:
            return ['SVG File Valid for Laser cutter']
        else:
            return ['SVG File Invalid. Errors:']+errors

class XMLNode:
    def __init__(self, parser, raw_data):
        self.data = raw_data
        self.parser = parser
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
                opening = (i, tag)
            if opening and (tag == '/'+opening[1] or tags[opening[0]].endswith('/>')):
                inner_text = ''
                if tag != opening[1]:
                    # Close the tag and pull all of the data in
                    inner_text = ''.join(tags[opening[0]+1:i])
                # If its a closing tag, then clip the tag type
                if tag.startswith('/'):
                    tag = tag[1:]
                # Add a top-level tag to the tag list
                if opening[1] == 'style':
                    styles = StyleNode(self.parser, inner_text)
                    styles.evaluate()
                else:
                    self.tags.append(TagNode(self.parser, tag, self.getAttributes(tags[opening[0]]), inner_text))
                opening = None
        # Iterate and parse each tag
        for tag in self.tags:
            # print(tag)
            tag.evaluate()
            # print(tag.errors)
            if tag.tag_type == "svg":
                viewbox = tag.attributes.get('viewBox')
                if viewbox:
                    self.width = viewbox.split()[2]
                else:
                    self.width = tag.attributes.get('width')
            self.errors += tag.errors

    def getAttributes(self, tag):
        tag = tag[1:-1]
        attrs = re.findall(r'[^ \t]+?=".+?"', tag)
        attr_dict = {}
        for a in attrs:
            a = a.strip().split('=')
            attr_dict[a[0]] = a[1][1:-1]
        return attr_dict

class TagNode:
    def __init__(self, parser, tag_type, attrs, inner_text):
        self.attributes = attrs
        self.tag_type = tag_type
        self.inner_text = inner_text
        self.errors = []
        self.parser = parser

    def __str__(self):
        return 'Tag(type={}, inner_text="{}", attributes="{}")'.format(self.tag_type, self.inner_text, self.attributes)

    def evaluate(self):
        '''
        Parse the attributes of the tag and check for validity
        '''
        if self.inner_text:
            node = XMLNode(self.parser, self.inner_text)
            node.evaluate()
            self.errors = node.errors
        extra_styles = self.parser.getStylesFor(self.tag_type, self.attributes)
        if 'style' in self.attributes:
            self.attributes['style'] += ';'.join(extra_styles)
        else:
            self.attributes['style'] = ';'.join(extra_styles)
        for a in self.attributes:
            if a != "style":
                self.checkAttribute(a, self.attributes[a])
            # Split the style up and parse those
            elif a == "style":
                styles = self.attributes[a].split(';')
                for style in styles:
                    if style:
                        style = style.split(':')
                        self.checkAttribute(*style)

    def checkAttribute(self, a, val):
        '''
        Check the attribute for validity
        '''
        val = val.lower()
        error = ''
        # find an invalid stroke colour attribute
        if a == "stroke":
            if val.lower() not in ('red', 'rgb(255, 0, 0)', '#ff0000', '#f00', 'blue', 'rgb(0, 0, 255)', '#0000ff', '#00f', "none"):
                error = 'Stroke colour is not RGB Red or RGB Blue'
        # Find an invalid fill colour attribute
        elif a == "fill":
            if val.lower() not in ('black', 'rgb(0, 0, 0)', "#000000", "none"):
                error = 'Fill colour is not Black'
        # Find an invalid stroke width attribute
        elif a == "stroke-width":
            if is_number(val) and eval(val) != 0.001:
                error = 'Incorrect stroke width'
        if error:
            if 'transform' in self.attributes and 'translate' in self.attributes['transform']:
                xy = re.findall('\(.+\)', self.attributes['transform'])[0]
                x, y = [float(a) for a in xy[1:-1].split()]
            elif self.tag_type == 'rect':
                x = float(self.attributes.get('x'))
                y = float(self.attributes.get('y'))
            elif self.tag_type != 'line':
                x = float(self.attributes.get('cx'))
                y = float(self.attributes.get('cy'))
            else:
                x = float(self.attributes.get('x1'))
                y = float(self.attributes.get('y1'))
            colour = 'black'# if self.getColour() != 'black' else 'white'
            name = self.attributes.get('id')
            class_name = self.attributes.get('class')
            if not name and not class_name:
                name = self.tag_type[0].upper()+self.tag_type[1:]
            if not name:
                name = class_name
            self.errors.append([[name, x, y, colour], error])

    def getColour(self):
        '''
        Get the fill colour of the object
        '''
        if self.attributes.get('fill'):
            c = self.attributes.get('fill')
        else:
            styles = self.attributes.get('style').split(';')
            c = ''
            for style in styles:
                if style:
                    style = style.split(':')
                    if style[0] == 'fill':
                        c = style[1]
                    if not c and style[0] == 'stroke':
                        c = style[1]
        if c.lower() in ['black', '#000000', '#000', 'rgb(0, 0, 0)', 'rgb(0,0,0)']:
            return 'black'
        else:
            return c

class StyleNode:
    def __init__(self, parser, inner_text):
        self.inner_text = inner_text[1:-1]
        self.style = {}
        self.parser = parser

    def __str__(self):
        return 'StyleNode(styles={})'.format(self.style)

    def evaluate(self):
        print(self.inner_text)
        self.inner_text = self.inner_text.replace('}', '}|')
        rules = [a.strip() for a in self.inner_text.split('|')]
        print(rules)
        for rule in rules:
            rule = [a for a in rule.split('{') if a]
            if not rule:
                continue
            identifiers = [a.strip() for a in rule[0].split(',')]
            style = rule[1][:-1]
            for i in identifiers:
                self.style[i] = self.style.get(i, '')+style
        print(self.style)
        self.parser.style = self.style


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
