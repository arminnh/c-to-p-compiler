from enum import Enum

offset = "    "

class ASTNode(object):

    def __init__(self, label="no label", parent=None):
        self.label = label
        self.children = [] # don't manipulate or read directly; use addChildNode and getChildren
        self.parent = parent

    def addChildNode(self, node):
        if not isinstance(node, ASTNode):
            raise Exception("trying to add child of non-ASTNode type: expected" + str(ASTNode) + ", got " + str(type(node)))
        self.children.append(node)
        node.parent = self
        return node

    def getChildren(self):
        return self.children

    def out(self, level=1):
        s = offset * level + self.label + "\n"

        s = self.outChildren(s, level)

        return s

    def outChildren(self, s, level):
        for child in self.getChildren():
            s += child.out(level+1)

        if not self.getChildren():
            s += "\n"

        return s

    # def __str__(self):
    #     return self.label

class ASTProgramNode(ASTNode):
    def __init__(self):
        super(ASTProgramNode, self).__init__("program")

class ASTHeaderNode(ASTNode):
    def __init__(self):
        self.stdIncludes = []
        self.customIncludes = []
        super(ASTHeaderNode, self).__init__("header")

    def out(self, level):
        s = offset * level + self.label + "\n"

        if self.stdIncludes:
            s += offset * level + "std includes:    " + str(self.stdIncludes) + "\n"

        if self.customIncludes:
            s += offset * level + "custom includes: " + str(self.customIncludes) + "\n"

        s = self.outChildren(s, level)

        return s

class ASTStdIncludeNode(ASTNode):
    def __init__(self):
        self.includeName = None
        super(ASTStdIncludeNode, self).__init__("stdInclude")

class ASTFunctionsNode(ASTNode):
    def __init__(self):
        super(ASTFunctionsNode, self).__init__("functions")

class ASTMainFunctionNode(ASTNode):
    def __init__(self):
        super(ASTMainFunctionNode, self).__init__("main")
        self.parameters = None

class ASTFunctionDeclarationNode(ASTNode):
    def __init__(self, label="functionDeclaration"):
        super(ASTFunctionDeclarationNode, self).__init__(label)
        self.type = None
        self.identifier = None
        # parameters are child nodes

    def out(self, level):
        s = offset * level + self.label + "\n"
        s += offset * (level+1) + "return type: " + self.type + "\n"
        s += offset * (level+1) + "identifier:  " + self.identifier + "\n\n"

        s = self.outChildren(s, level)

        return s

class ASTFunctionDefinitionNode(ASTFunctionDeclarationNode):
    def __init__(self):
        super(ASTFunctionDefinitionNode, self).__init__("functionDefinition")
        # parameters and statements are child nodes

class ASTParameterNode(ASTNode):
    def __init__(self):
        super(ASTParameterNode, self).__init__("parameter")
        self.type = None
        self.identifier = None
        self.isArray = False
        self.arrayLength = None
        # TODO: arrayLength can be an expressionNode -> change
        self.isConstant = False
        self.indirections = 0

    def out(self, level):
        s = offset * level + "parameter" + " | " + self.type

        if (self.isConstant != False) :
            s += " | const"

        s += " | " + self.identifier

        if (self.isArray != False) :
            s += " | array:  " + str(self.isArray)

            if (self.arrayLength != None) :
                s += " | arrayLength: " + str(self.arrayLength)

        s = self.outChildren(s, level)

        return s

class ASTParametersNode(ASTNode):
    def __init__(self):
        super(ASTParametersNode, self).__init__("parameters")

    def out(self, level):
        return super(ASTParametersNode, self).out(level) + "\n"

class ASTArgumentsNode(ASTNode):
    def __init__(self):
        super(ASTArgumentsNode, self).__init__("arguments")

    def out(self, level):
        return super(ASTArgumentsNode, self).out(level) + "\n"

    def outChildren(self, s, level):
        for child in self.getChildren():
            s += child.out(level+1)

        return s

'''
    STATEMENTS
'''

class ASTStatementsNode(ASTNode):
    def __init__(self):
        super(ASTStatementsNode, self).__init__("statements")

    def out(self, level=1):
        s = offset * level + self.label + "\n"

        if self.getChildren():
            s = self.outChildren(s, level)
        else:
            s += offset * (level+1) + "None\n\n"

        return s

class ASTStatementNode(ASTNode):
    def __init__(self, label="statement"):
        super(ASTStatementNode, self).__init__(label)

    def out(self, level=1):
        s = offset * level + self.label + "\n"
        s = ""

        s = self.outChildren(s, level-1)

        return s

class ASTIfNode(ASTStatementNode):
    def __init__(self):
        super(ASTIfNode, self).__init__("if")
        self.condition = None # expressionNode
        self.elseCondNode = None # elseNode

    def out(self, level):
        s = offset * level + self.label + "\n"

        for child in self.getChildren():
            if isinstance(child, ASTExpressionNode):
                s += offset * (level+1) + "condition\n"
                s += child.out(level+2)
            elif isinstance(child, ASTStatementNode):
                s += offset * (level+1) + "then\n"
                s += child.out(level+2)
            else:
                s += child.out(level+1)

        if not self.getChildren() and not isinstance(self.parent, ASTBinaryOperatorNode):
            s += "\n"

        return s

class ASTElseNode(ASTNode):
    def __init__(self):
        super(ASTElseNode, self).__init__("else")

    def out(self, level):
        return ASTNode.out(self, level)

class ASTWhileNode(ASTStatementNode):
    def __init__(self):
        super(ASTWhileNode, self).__init__("while")

    def out(self, level):
        return ASTNode.out(self,    level)

class ASTDoWhileNode(ASTStatementNode):
    def __init__(self):
        super(ASTDoWhileNode, self).__init__("doWhile")

    def out(self, level):
        return ASTNode.out(self,    level)

class ASTVariableDeclarationNode(ASTStatementNode):
    def __init__(self):
        super(ASTVariableDeclarationNode, self).__init__("variableDeclaration")
        self.type = None
        self.isConstant = False
        # declaratorInitializers are children

    def out(self, level):
        s  = offset * level + self.label + "\n"
        s += offset * (level+1) + "return type: " + self.type
        s += ", const:  " + str(self.isConstant) + "\n\n"

        s = self.outChildren(s, level)

        return s

class ASTDeclaratorInitializerNode(ASTNode):
    def __init__(self):
        super(ASTDeclaratorInitializerNode, self).__init__("declaratorInitializer")
        self.identifier = None
        self.isArray = False
        self.indirections = 0
        # arrayLength will be an expressionNode child

    def out(self, level):
        s  = offset * level + "declaratorInitializer" + "\n"
        s += offset * (level+1) + "identifier: " + self.identifier

        if (self.isArray != False) :
            s += " | array: " + str(self.isArray)

        s += "\n\n"

        for child in self.getChildren():
            if self.isArray and isinstance(child, ASTExpressionNode):
                s += offset * (level+1) + "arrayLength\n"
                s += child.out(level+2)
            elif isinstance(child, ASTExpressionNode):
                s += offset * (level+1) + "initialization value\n"
                s += child.out(level+2)
            else:
                s += child.out(level+1)

        if not self.getChildren():
            s += "\n"

        return s

class ASTReturnExpressionNode(ASTStatementNode):
    def __init__(self):
        super(ASTReturnExpressionNode, self).__init__("return")

    def out(self, level):
        return ASTNode.out(self,    level)


'''
    EXPRESSIONS
'''

class ASTExpressionNode(ASTNode):
    def __init__(self, label="expression"):
        super(ASTExpressionNode, self).__init__(label)

    def out(self, level=1):
        s = offset * level + self.label + "\n"
        s = ""

        s = self.outChildren(s, level-1)

        return s

# TODO: split into int and float literal classes
class ASTNumberLiteralNode(ASTExpressionNode):
    class NumberType(Enum):
        int = 1
        float = 2

        def __str__(self):
            if self == ASTNumberLiteralNode.NumberType['int']: return "int"
            if self == ASTNumberLiteralNode.NumberType['float']: return "float"
            return super(ASTNumberLiteralNode.NumberType, self).__str__()

    def __init__(self, value):
        print ("nope")
        exit()
        self.value = value
        super(ASTNumberLiteralNode, self).__init__(str(value) + "|" + str(self.type()))

    def value(self):
        return self.value

    def type(self):
        if type(self.value) == int: return ASTNumberLiteralNode.NumberType['int']
        if type(self.value) == float: return ASTNumberLiteralNode.NumberType['float']
        return None

class ASTIntegerLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super(ASTIntegerLiteralNode, self).__init__("int")
        self.value = value

    def out(self, level):
        s = offset * level + self.label + " | " + str(self.value) + "\n"

        if (isinstance(self.parent.parent, ASTStatementNode) or isinstance(self.parent.parent.parent, ASTVariableDeclarationNode)):
            s += "\n"

        return s

class ASTFloatLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super(ASTFloatLiteralNode, self).__init__("float")
        self.value = value

    def out(self, level):
        s = offset * level + self.label + " | " + str(self.value) + "\n"

        if (isinstance(self.parent.parent, ASTStatementNode)):
            s += "\n"

        return s

class ASTCharacterLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super(ASTCharacterLiteralNode, self).__init__("char")
        self.value = value

    def out(self, level):
        s = offset * level + self.label + " | " + self.value + "\n"

        if (isinstance(self.parent.parent, ASTStatementNode)):
            s += "\n"

        return s

class ASTStringLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super(ASTStringLiteralNode, self).__init__("char*")
        self.value = value

    def out(self, level):
        s = offset * level + self.label + " | " + self.value + "\n"

        if (isinstance(self.parent.parent, ASTStatementNode)):
            s += "\n"

        return s

class ASTVariableNode(ASTExpressionNode):
    def __init__(self, identifier):
        super(ASTVariableNode, self).__init__("variable")
        self.identifier = identifier

    def out(self, level):
        s = offset * level + self.label + " | " + self.identifier + "\n"

        if (isinstance(self.parent.parent, ASTStatementNode)):
            s += "\n"

        return s

class ASTFunctionCallNode(ASTExpressionNode):
    def __init__(self):
        super(ASTFunctionCallNode, self).__init__("function call")
        self.identifier = None

    def out(self, level):
        s = offset * level + self.label + " | " + self.identifier + "\n"

        s = self.outChildren(s, level)

        return s

'''
    EXPRESISSION OPERATIONS
'''

class ASTUnaryOperatorNode(ASTExpressionNode):
    class Type(Enum):
        prefix = 1
        postfix = 2

        def __str__(self):
            if self == ASTUnaryOperatorNode.Type['prefix']: return "prefix"
            if self == ASTUnaryOperatorNode.Type['postfix']: return "postfix"
            return super(ASTUnaryOperatorNode.Type, self).__str__()

    def __init__(self, operatorType, label):
        super(ASTUnaryOperatorNode, self).__init__(label)
        self.operand = None
        self.operatorType = operatorType

    def setOperand(self, op):
        self.operand = op

    def getOperand(self):
        return self.operand

    def addChildNode(self, node):
        if self.operand is None:
            self.operand = node
        else:
            raise Exception("I don't want a second child, I'm a unary operator node!")
        node.parent = self

        return node

    def addChild(self, label):
        raise Exception("Don't call me, I'm a unary operator node!")

    def getChildren(self):
        children = []
        if self.operand is not None: children.append(self.operand)
        return children

    def out(self, level=1):
        s = offset * level + self.label + "\n"

        s = self.outChildren(s, level)

        return s

    def outChildren(self, s, level):
        for child in self.getChildren():
            s += child.out(level+1)

        return s

class ASTBinaryOperatorNode(ASTExpressionNode):
    def __init__(self, label):
        super(ASTBinaryOperatorNode, self).__init__(label)
        self.firstOperand = None
        self.secondOperand = None

    def setFirstOperand(self, op):
        self.firstOperand = op

    def setSecondOperand(self, op):
        self.secondOperand = op

    def getFirstOperand(self):
        return self.firstOperand

    def getSecondOperand(self):
        return self.secondOperand

    def addChildNode(self, node):
        if self.firstOperand is None:
            self.firstOperand = node
        elif self.secondOperand is None:
            self.secondOperand = node
        else:
            raise Exception("I don't want a third child, I'm a binary operator node!")
        node.parent = self

        return node

    def addChild(self, label):
        raise Exception("Don't call me, I'm a binary operator node!")

    def getChildren(self):
        children = []
        if self.firstOperand is not None: children.append(self.firstOperand)
        if self.secondOperand is not None: children.append(self.secondOperand)
        return children

    def out(self, level=1):
        s = offset * level + self.label + "\n"

        s = self.outChildren(s, level)

        return s + "\n"

    def outChildren(self, s, level):
        for child in self.getChildren():
            s += child.out(level+1)

        return s

class ASTTernaryOperatorNode(ASTExpressionNode):
    def __init__(self, label):
        super(ASTTernaryOperatorNode, self).__init__(label)
        self.firstOperand = None
        self.secondOperand = None
        self.thirdOperand = None

    def setFirstOperand(self, op):
        self.firstOperand = op

    def setSecondOperand(self, op):
        self.secondOperand = op

    def setThirdOperand(self, op):
        self.thirdOperand = op

    def getFirstOperand(self):
        return self.firstOperand

    def getSecondOperand(self):
        return self.secondOperand

    def getThirdOperand(self):
        return self.thirdOperand

    def addChildNode(self, node):
        if self.firstOperand is None:
            self.firstOperand = node
        elif self.secondOperand is None:
            self.secondOperand = node
        elif self.thirdOperand is None:
            self.thirdOperand = node
        else:
            raise Exception("I don't want a fourth child, I'm a ternary operator node!")
        node.parent = self

        return node

    def addChild(self, label):
        raise Exception("Don't call me, I'm a ternary operator node!")

    def getChildren(self):
        children = []
        if self.firstOperand is not None: children.append(self.firstOperand)
        if self.secondOperand is not None: children.append(self.secondOperand)
        if self.thirdOperand is not None: children.append(self.thirdOperand)
        return children

    def out(self, level=1):
        s = offset * level + self.label + "\n"

        s = self.outChildren(s, level)

        return s

    def outChildren(self, s, level):
        for child in self.getChildren():
            s += child.out(level+1)

        return s

class ASTTernaryConditionalOperatorNode(ASTTernaryOperatorNode):
    def __init__(self):
        super(ASTTernaryConditionalOperatorNode, self).__init__("?:")

class ASTSimpleAssignmentOperatorNode(ASTBinaryOperatorNode):
    def __init__(self):
        super(ASTSimpleAssignmentOperatorNode, self).__init__("=")

class ASTLogicOperatorNode(ASTBinaryOperatorNode):
    class LogicOperatorType(Enum):
        conj = 1
        disj = 2

        def __str__(self):
            if self == ASTLogicOperatorNode.LogicOperatorType['conj']: return "and"
            if self == ASTLogicOperatorNode.LogicOperatorType['disj']: return "or"
            return super(ASTLogicOperatorNode.LogicOperatorType, self).__str__()

    def __init__(self, logicOperatorType):
        super(ASTLogicOperatorNode, self).__init__(str(logicOperatorType))
        self.logicOperatorType = logicOperatorType

class ASTComparisonOperatorNode(ASTBinaryOperatorNode):
    class ComparisonType(Enum):
        lt = 1
        gt = 2
        le = 3
        ge = 4
        equal = 5
        inequal = 6

        def __str__(self):
            if self == ASTComparisonOperatorNode.ComparisonType['lt']: return "<"
            if self == ASTComparisonOperatorNode.ComparisonType['gt']: return ">"
            if self == ASTComparisonOperatorNode.ComparisonType['le']: return "<="
            if self == ASTComparisonOperatorNode.ComparisonType['ge']: return ">="
            if self == ASTComparisonOperatorNode.ComparisonType['equal']: return "=="
            if self == ASTComparisonOperatorNode.ComparisonType['inequal']: return "!="
            return super(ASTComparisonOperatorNode.ComparisonType, self).__str__()

    def __init__(self, comparisonType):
        label = str(comparisonType)
        super(ASTComparisonOperatorNode, self).__init__(label)
        self.comparisonType = comparisonType

class ASTUnaryArithmeticOperatorNode(ASTUnaryOperatorNode):
    class ArithmeticType(Enum):
        increment = 1
        decrement = 2

        def __str__(self):
            if self == ASTUnaryArithmeticOperatorNode.ArithmeticType['increment']: return "++"
            if self == ASTUnaryArithmeticOperatorNode.ArithmeticType['decrement']: return "--"
            return super(ASTUnaryArithmeticOperatorNode, self).__str__()

    def __init__(self, arithmeticType, operatorType):
        super(ASTUnaryArithmeticOperatorNode, self).__init__(operatorType, str(arithmeticType) + "|" + str(operatorType))

class ASTAddressOfOperatorNode(ASTUnaryOperatorNode):
    def __init__(self):
        super(ASTAddressOfOperatorNode, self).__init__("&", ASTUnaryOperatorNode.Type['prefix'])

class ASTDereferenceOperatorNode(ASTUnaryOperatorNode):
    def __init__(self):
        super(ASTDereferenceOperatorNode, self).__init__("*", ASTUnaryOperatorNode.Type['prefix'])

class ASTLogicalNotOperatorNode(ASTUnaryOperatorNode):
    def __init__(self):
        super(ASTLogicOperatorNode, self).__init__("!", ASTUnaryOperatorNode.Type['prefix'])

class ASTBinaryArithmeticOperatorNode(ASTBinaryOperatorNode):
    class ArithmeticType(Enum):
        add = 1
        sub = 2
        mul = 3
        div = 4
        remainder = 5

        def __str__(self):
            if self == ASTBinaryArithmeticOperatorNode.ArithmeticType['add']: return "+"
            if self == ASTBinaryArithmeticOperatorNode.ArithmeticType['sub']: return "-"
            if self == ASTBinaryArithmeticOperatorNode.ArithmeticType['mul']: return "*"
            if self == ASTBinaryArithmeticOperatorNode.ArithmeticType['div']: return "/"
            if self == ASTBinaryArithmeticOperatorNode.ArithmeticType['remainder']: return "%"
            return super(ASTBinaryArithmeticOperatorNode.ArithmeticType, self).__str__()

    def __init__(self, arithmeticType):
        label = str(arithmeticType)
        ASTBinaryOperatorNode.__init__(self, label)
        self.arithmeticType = arithmeticType


'''
    AST
'''

class AbstractSyntaxTree:

    def __init__(self, root=ASTNode("root")):
        self.root = root

    def __str__(self):
        return "AST:\n" + self.root.out()

'''
    TESTS
'''

if __name__=="__main__":
    root = ASTNode("root")

    one = root.addChild("child1")
    two = root.addChild("child2")

    three = one.addChild("three")

    four = two.addChild("four")
    five = two.addChild("five")

    three.addChild("six")

    ast = AbstractSyntaxTree(root)
    print (root.out())

    currentNode = root
    print (currentNode)
    print (currentNode.parent)
    currentNode = currentNode.addChild("bla")
    print (currentNode)
    print (currentNode.parent)
    currentNode = currentNode.addChild("blabla")
    print (currentNode)
    print (currentNode.parent)
    currentNode = currentNode.parent
    print (currentNode)
    print (currentNode.parent)
