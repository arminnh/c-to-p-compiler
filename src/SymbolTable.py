from AbstractSyntaxTree import *
from CompilerErrorHandler import *

offset = "    "

class SymbolInfo:
    def __init__(self, astnode):
        self.astnode = astnode
        self.typeInfo = astnode.getType()

class VariableSymbolInfo(SymbolInfo):
    def __init__(self, astnode):
        # astnode is ASTDeclaratorInitializerNode
        super(VariableSymbolInfo, self).__init__(astnode)

    @property
    def defined(self):
        for child in self.astnode.children:
            if isinstance(child, ASTExpressionNode):
                return True
        return False


class FunctionSymbolInfo(SymbolInfo):
    def __init__(self, astnode):
        super(FunctionSymbolInfo, self).__init__(astnode)

    @property
    def defined(self):
        return isinstance(self.astnode, ASTFunctionDefinitionNode)


class Scope:
    def __init__(self, parent=None, name=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.symbols = {}

    def addChild(self, name=None):
        new = Scope(self, name)
        self.children.append(new)
        return new

    def insertSymbol(self, info:SymbolInfo, errorHandler:CompilerErrorHandler):
        if self.isInsertionOk(info, errorHandler):
            #print("inserted id " + str(info.astnode.identifier) + " into symbol table")
            self.symbols[info.astnode.identifier] = info

    def retrieveSymbol(self, name):
        if name is None:
            return None
        return self.symbols.get(name)

    def isInsertionOk(self, new:SymbolInfo, errorHandler:CompilerErrorHandler):
        old = self.retrieveSymbol(new.astnode.identifier)

        if old is not None:
            if isinstance(old.astnode, ASTDeclaratorInitializerNode):
                line, column = new.astnode.getLineAndColumn()
                errorHandler.addError("Identifier {0} already taken by variable".format(old.astnode.identifier), line, column)
                return False

            if type(new) is FunctionSymbolInfo:
                if isinstance(new.astnode, ASTFunctionDefinitionNode):
                    if type(old.astnode) is ASTFunctionDeclarationNode:
                        if old.astnode.getParameters() == new.astnode.getParameters():
                            return True # definition can overwrite declaration
                        else:
                            line, column = new.astnode.getLineAndColumn() # TODO: get line, column of old declaration as well
                            errorHandler.addError("Function definition parameters don't match with previous declaration", line, column)
                            return False

                    elif isinstance(old.astnode, ASTFunctionDefinitionNode):
                        if not old.astnode.getType().isCompatible(new.astnode.getType()):
                            line, column = new.astnode.getLineAndColumn()
                            errorHandler.addError("Conflicting types for function definition '{0}'".format(str(new.astnode.identifier)), line, column)
                            return False
                        else:
                            line, column = new.astnode.getLineAndColumn()
                            errorHandler.addError("Redefinition of function '{0}'".format(new.astnode.identifier), line, column)
                            return False

                elif isinstance(new.astnode, ASTFunctionDeclarationNode):
                    if type(old.astnode) is ASTFunctionDefinitionNode:
                        if not old.astnode.getType().isCompatible(new.astnode.getType()):
                            line, column = new.astnode.getLineAndColumn()
                            errorHandler.addError("Conflicting types for function declaration " + str(new.astnode.identifier), line, column)
                            return False

                        if old.astnode.getParameters() == new.astnode.getParameters():
                            return False # declaration cannot overwrite definition
                        else:
                            line, column = new.astnode.getLineAndColumn()
                            errorHandler.addError("Function declaration parameters don't match previous definition", line, column)
                            return False

                    elif type(old.astnode) is ASTFunctionDeclarationNode:
                        if old.astnode.getParameters() == new.astnode.getParameters():
                            return False # declaration cannot overwrite definition
                        else:
                            line, column = new.astnode.getLineAndColumn()
                            errorHandler.addError("Function declaration parameters don't match previous declaration", line, column)
                            return False

            elif type(new) is VariableSymbolInfo:
                line, column = old.astnode.getLineAndColumn()
                errorHandler.addError("Identifier {0} already taken by function".format(old.astnode.identifier), line, column)
                return False

        else:
            return True


    def out(self, level):
        out = offset * level + "Scope" + (" " + self.name if self.name is not None else "") + ":\n"
        for key, value in self.symbols.items():
            out += offset * (level + 1) + str(key) + ": " + str(value.astnode.getType()) + "\n"

        for child in self.children:
            out += child.out(level + 1)

        return out

class SymbolTable(object):
    def __init__(self):
        self.root = Scope()
        self.currentScope = self.root

    def openScope(self, name=None):
        self.currentScope = self.currentScope.addChild(name)

    def closeScope(self):
        self.currentScope = self.currentScope.parent

    def insertVariableSymbol(self, astnode, errorHandler:CompilerErrorHandler):
        self.currentScope.insertSymbol(VariableSymbolInfo(astnode), errorHandler)

    def insertFunctionSymbol(self, astnode, errorHandler:CompilerErrorHandler):
        self.currentScope.insertSymbol(FunctionSymbolInfo(astnode), errorHandler)

    def retrieveSymbol(self, name):
        scope = self.currentScope
        while scope is not None:
            nametype = scope.retrieveSymbol(name)
            if nametype is not None:
                return nametype
            scope = scope.parent

    def __str__(self):
        return self.root.out(0)
