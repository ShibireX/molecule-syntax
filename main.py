from linkedQFile import LinkedQ
import sys
from molgrafik import Molgrafik


class Ruta:
    def __init__(self, atom="()", num=1, mass=0):
        self.atom = atom
        self.num = num
        self.mass = mass
        self.next = None
        self.down = None

    def weight(self):
        weight = self.mass * self.num
        if self.next:
            weight += self.next.weight()
        if self.down:
            weight += self.down.weight() * self.num

        return weight


class Syntaxfel(Exception):
    pass


def readMol(q, paranthesis_queue):
    mol = readGroup(q, paranthesis_queue)
    if not q.peek():
        return mol

    elif q.peek() == ")":
        if not paranthesis_queue.peek():
            raise Syntaxfel("Felaktig gruppstart vid radslutet ")
        return mol

    else:
        mol.next = readMol(q, paranthesis_queue)
        return mol


def readGroup(q, paranthesis_queue):
    rutan = Ruta()

    if not q.peek():
        raise Syntaxfel("Felaktig gruppstart vid radslutet ")

    elif q.peek().isnumeric():
        raise Syntaxfel("Felaktig gruppstart vid radslutet ")

    elif q.peek().isalpha():
        rutan.atom, rutan.mass = readAtom(q)
        if not q.peek():
            return rutan
        if q.peek().isnumeric():
            rutan.num = readNum(q)
        return rutan

    elif q.peek() == "(":
        paranthesis_queue.enqueue(q.dequeue())

        if q.peek().isnumeric():
            raise Syntaxfel("Felaktig gruppstart vid radslutet ")

        rutan.down = readMol(q, paranthesis_queue)
        if not q.peek() == ")":
            raise Syntaxfel("Saknad högerparentes vid radslutet ")

        paranthesis_queue.dequeue()
        q.dequeue()

        if not q.peek():
            raise Syntaxfel("Saknad siffra vid radslutet ")
        rutan.num = readNum(q)

        return rutan

    raise Syntaxfel("Felaktig gruppstart vid radslutet ")


def readAtom(q):

    atoms_dict = {'H': 1.00794, 'He': 4.002602, 'Li': 6.941, 'Be': 9.012182, 'B': 10.811,
                  'C': 12.0107, 'N': 14.0067, 'O': 15.9994, 'F': 18.9984032, 'Ne': 20.1797, 'Na': 22.98976928,
                 'Mg': 24.3050, 'Al': 26.9815386, 'Si': 28.0855, 'P': 30.973762, 'S': 32.065, 'Cl': 35.453,
                  'Ar': 39.948, 'K': 39.0983, 'Ca': 40.078, 'Sc': 44.955912, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961,
                 'Mn': 54.938045, 'Fe': 55.845, 'Co': 58.933195, 'Ni': 58.6934, 'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723,
                  'Ge': 72.64, 'As': 74.92160, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.798,
                 'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.90585, 'Zr': 91.224, 'Nb': 92.90638, 'Mo': 95.96,
                  'Tc': 98, 'Ru': 101.07, 'Rh': 102.90550, 'Pd': 106.42, 'Ag': 107.8682, 'Cd': 112.411,
                 'In': 114.818, 'Sn': 118.710, 'Sb': 121.760, 'Te': 127.60, 'I': 126.90447, 'Xe': 131.293,
                  'Cs': 132.9054519, 'Ba': 137.327, 'La': 138.90547, 'Ce': 140.116, 'Pr': 140.90765, 'Nd': 144.242,
                 'Pm': 145, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25, 'Tb': 158.92535, 'Dy': 162.500, 'Ho': 164.93032,
                  'Er': 167.259, 'Tm': 168.93421, 'Yb': 173.054, 'Lu': 174.9668, 'Hf': 178.49,
                 'Ta': 180.94788, 'W': 183.84, 'Re': 186.207, 'Os': 190.23, 'Ir': 192.217, 'Pt': 195.084,
                  'Au': 196.966569, 'Hg': 200.59, 'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.98040, 'Po': 209,
                 'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232.03806, 'Pa': 231.03588,
                  'U': 238.02891, 'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247,
                 'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257, 'Md': 258, 'No': 259, 'Lr': 262, 'Rf': 265, 'Db': 268,
                  'Sg': 271, 'Bh': 272, 'Hs': 270,
                 'Mt': 276, 'Ds': 281, 'Rg': 280, 'Cn': 285, 'Fl': 289, 'Lv': 293}

    readLetterUpper(q)
    atom = q.dequeue()

    if q.peek():
        if q.peek().islower():
            extension = readLetterLower(q)
            atom = atom + extension

    if atom in atoms_dict:
        return atom, atoms_dict[atom]

    raise Syntaxfel("Okänd atom vid radslutet ")


def readLetterUpper(q):
    if q.peek().isalpha() and q.peek().isupper():
        return

    raise Syntaxfel("Saknad stor bokstav vid radslutet ")


def readLetterLower(q):
    return q.dequeue()


def readNum(q):
    num = ""

    if q.peek().isnumeric():

        if q.peek() == "0":
            q.dequeue()
            raise Syntaxfel("För litet tal vid radslutet ")

        elif q.peek() == "1":
            num += q.dequeue()
            if q.peek():
                if not q.peek().isnumeric():
                    raise Syntaxfel("För litet tal vid radslutet ")
            else:
                raise Syntaxfel("För litet tal vid radslutet ")

        while q.peek():
            if q.peek().isnumeric():
                num += q.dequeue()
            else:
                break

        return int(num)

    raise Syntaxfel("Saknad siffra vid radslutet ")


def storeFormula(formula):
    q = LinkedQ()
    for symbol in formula:
        q.enqueue(symbol)

    return q


def checkFormula(formula):
    q = storeFormula(formula)
    paranthesis_queue = LinkedQ()

    try:
        mol = readMol(q, paranthesis_queue)
        return mol

    except Syntaxfel as fel:
        return str(fel) + str(q)




def main():
    mg = Molgrafik()
    formula = sys.stdin.readline().strip()

    while formula != "#":
        result = checkFormula(formula)
        print(result.weight())
        mg.show(result)
        formula = sys.stdin.readline().strip()


main()
