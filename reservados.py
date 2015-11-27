class PaReservados:
    reserverC = [
        "#", "include", "scanf", "alignas", "alignof","and", "and_eq", "asm",
        "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char",
        "char16_t", "char32_t", "class", "compl", "const", "constexpr", "const_cast",
        "continue", "decltype", "default", "delete", "do", "double", "dynamic_cast",
        "else", "explicit", "export", "extern", "enum", "false", "float", "for", "friend",
        "goto", "if", "int", "inline", "int", "long", "main", "mutable", "namespace", "new",
        "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "print", "printf",
        "private", "protected", "public", "register", "reinterpret_cast", "return", "short",
        "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch",
        "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid",
        "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t",
        "while", "xor", "xor_eq"]
    caracEspeciais = [1, 2, 3, 4, 5, 6, 7, 8, 9, ".", ",","=",";",":"]
    opAritimeticos = ["+", "-", "*", "/", "^"]
    opRelacionais = [">", "<", "==", "<>", ">=", "<="]
    opLogicos = ["and", "or", "not", "&"]
    expArit = ["(",")","[","]","{","}"]
    reservados = reserverC + opAritimeticos + opRelacionais + opLogicos + expArit + caracEspeciais

    a = "all(*.*)","txt(*.txt)","C(*.c)","C++(*.cpp)"
    tipos = ""
    for x in a:
        tipos += "%s" % x + "\n"