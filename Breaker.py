import Seleni


to_break = input("Veuillez renseigner le texte crypté que vous tentez de casser.\n\nTexte : ")
element = (input("\n\n\nQuel mot savez-vous présent dans le message ?\nMot : ")).lower()
iterations = int(input("\n\nCombien de tests voulez-vous faire ?\n(Vous pouvez à tout moment interrompre par : [Controle + C])\nNombre : "))

number = 1

results = []

try : 
    while True : 
        try : 
            t = Seleni.decrypt(number, to_break)
        except Seleni.HasGivenTextError : 
            pass

        if element in t.lower() : 
            print("\n")
            print(f"{number} : {t}")
            results.append(t)
        else : 
            print(f"{number} : {t}")

        if number > iterations : 
            break

        number += 1
        
    
except KeyboardInterrupt : 
    print(f"\n\n\nNombre de clefs testées : {number}.\n\nRésultats trouvés : ")
    for r in results : 
        print(f"\n[{r}]")
else : 
    print(f"\n\n\nNombre de clefs testées : {number}.\n\nRésultats trouvés : ")
    for r in results : 
        print(f"\n[{r}]")