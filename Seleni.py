__version__ = "1.3.2.0"


class HasNoTextError(Exception):
    def __init__(self):
        self.message = "|> 'error': 'NoTextError'"

    def __str__(self):
        return self.message


class HasNoKeyError(Exception):
    def __init__(self):
        self.message = "|> 'error': 'KeyError'"

    def __str__(self):
        return self.message


class HasGivenTextError(Exception):
    def __init__(self, detail="'Unknow error'"):
        self.message = f"|> 'error': 'GivenTextError', 'details': {detail}"

    def __str__(self):
        return self.message


def Verify_HasNoTextError(str_text):  # Vérifie si le texte est vide.
    if (str_text == "") or (str_text is None):
        raise HasNoTextError()
    else:
        return False


def Verify_HasNoKeyError(str_key):  # Vérifie si la clé est vide.
    if (str_key == "") or (str_key is None):
        raise HasNoKeyError()
    else:
        return False


# Vérifie si le texte donné pour le déchiffrement n'est pas chiffré.
def Verify_HasGivenTextError(str_text, error_detail="This text is not encoded by Seleni"):
    list_text = list(str_text)
    for i in range(len(list_text)):
        traitement = list_text[i]
        if traitement != ".":
            passage = False
            for o in range(10):
                if traitement == str(o):
                    passage = True
            if passage is False:
                raise HasGivenTextError()
    return False


# Plus le nombre est grand, plus il supporte de caractères mais plus le texte codé est long (pour 8 192, chaque caractère peut faire jusqu'a 8192)
# Nombre de chiffre maximal par caractère. 3 est suffisant pour tous les caractères normaux.
prise_en_charge = 7
# 8388608 (prise-en-charge = 7) : Un multiple de 2 très élevé qui, je l'espère, prend en compte tous les caractères possibles.

modulo = 2
# Répéter jusqu'a ce que modulo soit un multiple de 2 de cettes chiffres.
while not(len(list(str(modulo))) > prise_en_charge):
    modulo *= 2
modulo //= 2  # On divise par deux car le while s'arrête une fois trop tard.


def inversion_modulaire(a, b):  # Inverse de b modulo a
    r, u, o, s, w, x = a, 1, 0, b, 0, 1
    while s != 0:
        q = r // s
        r, u, o, s, w, x = s, w, x, r - q*s, u - q*w, o - q*x
    if r != 1:
        return False
    else:
        y = o
        if y < 0:
            while y < 0:
                y = y + a
        return y


def crypt(key, text):
    Verify_HasNoTextError(text)
    Verify_HasNoKeyError(key)

    len_key = len(key)

    # Convertir le texte clair en chiffres
    text = list(text)
    for caract in range(len(text)):
        # Transforme chaque caractère du texte (une liste) en chiffres ASCII.
        text[caract] = str(ord(text[caract]))
        # Si le caractère n'est pas pris en charge.
        if int(text[caract]) > modulo:
            print("\nCaractère [{}] non pris en charge. Equivalent ASCII : [{}] Transformé en [~]\n".format(
                chr(int(text[caract])), text[caract]))
            text[caract] = "126"  # Alors il est transformé en ~

    # Convertir la clé texte en chiffres (si elle ne l'est pas encore).
    try:
        temp_test_key = int(key)
        if temp_test_key < 0:  # Si la clée est un nombre négatif.
            del (temp_test_key)
            # Déclenche l'exception et prend la clée en tant que clée texte.
            raise ValueError
        else:
            del (temp_test_key)
        # C'est donc une clé Numérique car int(key) ne renvoie pas d'erreur
        key = list(key)
    except ValueError:
        # C'est donc une clé texte.
        # Convertir la clé texte en clé numérique :
        key = list(key)

        for caract in range(len_key):
            key[caract] = str(ord(key[caract]))

    # (↓) Définir les blocs (chiffrement par blocs)

    # Ajouter des espaces de façon a ce que le texte soit divisible en le nombre de blocs
    for i in range(len_key):
        # Si le texte a crypter plus i est divisible par la longueur de la clé :
        if (len(text) + i) % len_key == 0:
            number_of_blocks = int((len(text) + i) / len_key)
            for z in range(i):
                text.append(str(ord(" ")))
            break

    for block_number in range(number_of_blocks):
        # Un bloc = la longueur de la clé
        for position_in_block in range(len_key):
            # Caract = position du caractère
            caract = position_in_block + (block_number * len_key)
            # \\ Début du coeur du chiffrement
            # Cela veut donc dire que le nombre est pair.
            if int(key[position_in_block]) % 2 == 0:
                # On ajoute 1 au caractère traité de la clé pour qu'il devienne impair.
                key[position_in_block] = str(int(key[position_in_block]) + 1)
            # Chiffrement modulo 1
            text[caract] = int(text[caract]) * int(key[position_in_block])
            # Chiffrement modulo 2 (% signifie modulo)
            text[caract] = text[caract] % modulo
            # Décalage de fréquence : ajoute i (place dans le bloc) au caractère
            text[caract] = str(int(text[caract]) + position_in_block)
            # // Fin du coeur du chiffrement
        # Todo

    str_crypted_text = ".".join(text)
    return str_crypted_text  # Retourne le texte crypté.


def decrypt(key, text):
    text = text.strip()

    Verify_HasNoTextError(text)
    Verify_HasNoKeyError(key)
    Verify_HasGivenTextError(text, "This text is not encoded by Seleni")

    len_key = len(key)

    text = text.split(".")  # Convertit en une liste et retire les points.

    # Convertir la clé texte en chiffres (si elle ne l'est pas encore).
    try:
        temp_test_key = int(key)
        if temp_test_key < 0:  # Si la clée est un nombre négatif.
            del (temp_test_key)
            # Déclenche l'exception et prend la clée en tant que clée texte.
            raise ValueError
        else:
            del (temp_test_key)
        # C'est donc une clé Numérique car int(key) ne renvoie pas d'erreur
        key = list(key)
    except ValueError:
        # C'est donc une clé texte.
        # Convertir la clé texte en clé numérique :
        key = list(key)

        for caract in range(len_key):
            key[caract] = str(ord(key[caract]))

    # (↓) Définir les blocs (chiffrement par blocs)

    number_of_blocks = int(len(text) / len_key)

    for block_number in range(number_of_blocks):
        # Un bloc = la longueur de la clé
        for position_in_block in range(len_key):
            caract = position_in_block + (block_number * len_key)
            # \\ Début du coeur du chiffrement
            # Décalage de fréquence : enlève position dans le bloc au caractère
            text[caract] = str(int(text[caract]) - position_in_block)
            # Cela veut donc dire que le nombre est pair.
            if int(key[position_in_block]) % 2 == 0:
                # On ajoute 1 au caractère traité de la clé pour qu'il devienne impair.
                key[position_in_block] = str(int(key[position_in_block]) + 1)
            # invers_mod_key est le nombre qui permet de déchiffrer le chiffrement modulo.
            invers_mod_key = inversion_modulaire(
                modulo, int(key[position_in_block]))
            text[caract] = int(text[caract]) * \
                invers_mod_key  # Déchiffrement modulo 1
            # Déchiffrement modulo 2 (% signifie modulo)
            text[caract] = text[caract] % modulo
            # // Fin du coeur du chiffrement
    # Todo

    try:
        for caract in range(len(text)):
            # Transforme chaque chiffre ASCII du texte (une liste) en lettres.
            text[caract] = str(chr(int(text[caract])))
    except ValueError:
        raise HasGivenTextError(detail="Valeurs incorrectes")

    # Enlever des espaces ajoutés de façon a ce que le texte soit divisible en le nombre de blocs
    try:
        for i in range(len(text)):
            traitement = -1
            if text[traitement] == " ":
                del (text[traitement])  # Supprime les espaces ajoutés.
            elif text[traitement] == "\n":
                # Supprime les retour à la ligne ajoutés (\n en python)
                del (text[traitement])
            elif text[traitement] != "":
                break  # Quitte
            else:
                # Supprime les retour à la ligne ajoutés (\n en python)
                del (text[traitement])
    except IndexError:
        pass

    str_decrypted_text = "".join(text)
    return str_decrypted_text  # Retourne le texte décrypté.
