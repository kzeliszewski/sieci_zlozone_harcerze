from pyvis.network import Network
import matplotlib.pyplot as plt
import random

# Funkcja tworząca sieć wyjściową
def initialize_network():
    net = Network(notebook=True)
    net.toggle_physics(True)
    net.show_buttons(filter_=["physics"])
    net.force_atlas_2based()

    # Tworzenie węzłów
    for i in range(51):
        # Tworzenie gromady zuchowej
        if 0 <= i < 15:
            age = random.randint(6, 9)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="harcerz", color="#7a7d80")
        # Tworzenie drużyny harcerskiej
        if 15 <= i < 27:
            age = random.randint(10, 12)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="harcerz", color="#7a7d80")
        # Tworzenie drużyny starszoharcerskiej
        if 27 <= i < 35:
            age = random.randint(13, 15)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="harcerz", color="#7a7d80")
        # Tworzenie drużyny wędrowniczej
        if 35 <= i < 40:
            age = random.randint(16, 21)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="harcerz", color="#7a7d80")
        # Tworzenie instruktorów w stopniu przewodnika
        if 40 <= i < 47:
            age = random.randint(16, 25)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="przewodnik", color="#0f2858")
        # Tworzenie instruktorów w stopniu podharcmistrza
        if 47 <= i < 50:
            age = random.randint(18, 35)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="podharcmistrz", color="#0a5c0a")
        # Tworzenie harcmistrza
        if 50 <= i < 51:
            age = random.randint(21, 50)
            net.add_node(n_id=i, label=age, title=f"Wiek: {age}", group="harcmistrz", color="#ff0000")
    # Tworzenie krawędzi
    # Lączymy relacjami członków drużyny z członkami ich drużyny z nimi sąsiadującymi oraz z drużynowym
    for g in range(15):
        net.add_edge(g, 40)
    for g in range(14):
        net.add_edge(g, g+1)
    net.add_edge(14, 0)

    for g in range(15, 27):
        net.add_edge(g, 41)
    for g in range(15, 26):
        net.add_edge(g, g+1)
    net.add_edge(26, 15)

    for g in range(27, 35):
        net.add_edge(g, 42)
    for g in range(27, 34):
        net.add_edge(g, g+1)
    net.add_edge(34, 27)

    for g in range(35, 40):
        net.add_edge(g, 43)
    for g in range(35, 39):
        net.add_edge(g, g+1)
    net.add_edge(39, 35)
    # Lączymy relacją przewodników pomiędzy sąsiadami
    for g in range(40, 47):
        net.add_edge(g, g+1)
    net.add_edge(46, 40)
    # Lączymy podharcmistrzow z sasiadami i z harcmistrzem
    for g in range(47, 49):
        net.add_edge(g, g+1)
        net.add_edge(g, 50)
    # Dodajemy połączenia pomiędzy instruktorami
    net.add_edge(49, 47)
    net.add_edges([(40, 47), (40, 48), (41, 48), (41, 49), (42, 49), (43, 47), (43, 48), (44, 49), (45, 49), (46, 47),
                   (46, 49), (49, 50)])

    return net

def stopien_wezla(net, id):
    stopien = 0
    for krawedz in net.edges:
        if id == krawedz['from'] or id == krawedz['to']:
            stopien += 1
    return stopien

# Prawdopodobieństwo opuszczenia organizacji
def prawdopodobienstwo_usuniecia(wiek, stopien):
    if wiek < 25:
        p = (0.6 - wiek / 100) / stopien
    else:
        p = (wiek / 100) / stopien
    return p


def czy_istnieje_krawedz(net, id1, id2):
    if id1 == id2:
        return False
    for krawedz in net.edges:
        if id1 == krawedz['from'] and id2 == krawedz['to']:
            return True
        elif id1 == krawedz['to'] and id2 == krawedz['from']:
            return True
    return False

# Prawdopodobieństwo zwerbowania nowych członków przez przewodnika
def prawdopodobienstwo_dodania(stopien):
    p = 0.3 + stopien/100
    return p


def polaczenia(siec, id):
    polaczone_wierzcholki = []
    for krawedz in siec.edges:
        if id == krawedz['from']:
            polaczone_wierzcholki.append(krawedz['to'])
        elif id == krawedz['to']:
            polaczone_wierzcholki.append(krawedz['from'])
    return polaczone_wierzcholki


# Prawdopodobieństwo zmiany stanu (zdobycia stopnia)
def prawdopodobienstwo_zmiana(wiek, stopien, stan):
    if stan == 'harcerz':
        p = 0.5 + (wiek / 100) + (stopien / 50)
    elif stan == 'przewodnik':
        p = 0.01 + (wiek / 100) + (stopien / 300)
    elif stan == 'podharcmistrz':
        p = 0.05 + (wiek / 200) + (stopien / 500)
    else:
        p = 0
    return p


def zmiana_indeksow(siec, liczba):
    for i in range(liczba):
        siec.nodes[i]['id'] = i
    return siec


# Inicjalizacja
siec = initialize_network()
siec.show("network_frame0.html")


id_gen = 51
liczba_zuchow = []
liczba_harcerzy_m = []
liczba_hs = []
liczba_w = []
liczba_star = []
liczba_harcerzy = []
liczba_przewodnikow = []
liczba_podharcmistrzow = []
liczba_harcmistrzow = []
liczba_czlonkow = []
liczba_czlonkow2 = []
siec_lista = []
lista_nowych_harcerzy = []
lista_nowych_przewodnikow = []
lista_nowych_podharcmistrzow = []
lista_nowych_harcmistrzow = []
lista_usun = []
liczba_kadry = []
relacje = []

for rok in range(10):
    h, pwd, phm, hm = 0, 0, 0, 0
    z, har_m, hs, w, star = 0, 0, 0, 0, 0
    usun = 0
    nowy_h, nowy_pwd, nowy_phm, nowy_hm = 0, 0, 0, 0
    wezel = 1
    dlugosc = len(siec.nodes)
    liczba_czlonkow.append(len(siec.nodes))
    # Zbieramy statystyki na start roku
    while wezel < dlugosc:
        # Stany
        if siec.nodes[wezel]['group'] == 'harcerz':
            h += 1
        if siec.nodes[wezel]['group'] == 'przewodnik':
            pwd += 1
        if siec.nodes[wezel]['group'] == 'podharcmistrz':
            phm += 1
        if siec.nodes[wezel]['group'] == 'harcmistrz':
            hm += 1
        # Grupy wiekowe
        if 7 <= siec.nodes[wezel]['label'] < 10:
            z += 1
        if 10 <= siec.nodes[wezel]['label'] < 13:
            har_m += 1
        if 13 <= siec.nodes[wezel]['label'] < 16:
            hs += 1
        if 16 <= siec.nodes[wezel]['label'] < 22:
            w += 1
        if siec.nodes[wezel]['label'] >= 22:
            star += 1

        # Sprawdzanie stopnia węzła
        id_wezla = siec.nodes[wezel]['id']
        stopien = stopien_wezla(siec, id_wezla)

        lista_polaczen = polaczenia(siec, id_wezla)
        # Wiek wezla
        wiek = siec.nodes[wezel]['label']

        # Usuwanie węzła
        prawdopodobienstwo = random.uniform(0, 1)
        if prawdopodobienstwo < prawdopodobienstwo_usuniecia(wiek, stopien):
            siec.nodes.remove(siec.nodes[wezel])
            dlugosc -= 1
            usun += 1
        else:
            # Dodawanie krawędzi
            liczba_krawedzi = random.randint(0, 2)
            for i in range(liczba_krawedzi):
                losowy_wezel = random.randint(0, len(siec.nodes)-1)
                if not czy_istnieje_krawedz(siec, id_wezla, siec.nodes[losowy_wezel]['id']):
                    siec.add_edge(id_wezla, siec.nodes[losowy_wezel]['id'])

            # Dodawanie nowych węzłów
            if siec.nodes[wezel]['group'] == 'przewodnik':
                prawdopodobienstwo2 = random.uniform(0, 1)
                liczba_nowych = random.randint(1, 6)
                if prawdopodobienstwo2 < prawdopodobienstwo_dodania(stopien_wezla(siec, id_wezla)):
                    for i in range(liczba_nowych):
                        age = random.randint(7, 15)
                        id_nowego = id_gen
                        id_gen += 1
                        siec.add_node(n_id=id_nowego, label=age, title=f"Wiek: {age}", group="harcerz", color="#7a7d80")
                        siec.add_edge(id_wezla, id_nowego)
                        nowy_h += 1
                        # Dodawanie krawedzi dla nowego wezla
                        liczba_krawedzi2 = random.randint(1, 3)
                        for i in range(liczba_krawedzi2):
                            losowy_wezel = random.randint(0, len(siec.nodes)-1)
                            if not czy_istnieje_krawedz(siec, id_nowego, siec.nodes[losowy_wezel]['id']):
                                siec.add_edge(id_nowego, siec.nodes[losowy_wezel]['id'])

            #Sprawdzenie z jakimi stanami łączy się węzeł
            wartosc_polaczen = 0
            for j in range(len(lista_polaczen)):
                i = lista_polaczen[j]
                for g in range(len(siec.nodes)):
                    if siec.nodes[g]['id'] == i and siec.nodes[g]['group'] == 'podharcmistrz' and wartosc_polaczen < 2:
                        wartosc_polaczen = 1
                    elif siec.nodes[g]['id'] == i and siec.nodes[g]['group'] == 'harcmistrz':
                        wartosc_polaczen = 2

            # Zmiana stanu
            if siec.nodes[wezel]['group'] == 'harcerz' and wiek >= 16 and wartosc_polaczen > 0:
                prawdopodobienstwo3 = random.uniform(0, 1)
                if prawdopodobienstwo3 < prawdopodobienstwo_zmiana(wiek, stopien, siec.nodes[wezel]['group']):
                    siec.nodes[wezel]['group'] = 'przewodnik'
                    siec.nodes[wezel]['color'] = '#0f2858'
                    nowy_pwd += 1
            elif siec.nodes[wezel]['group'] == 'przewodnik' and wiek >= 18 and wartosc_polaczen > 1:
                prawdopodobienstwo3 = random.uniform(0, 1)
                if prawdopodobienstwo3 < prawdopodobienstwo_zmiana(wiek, stopien, siec.nodes[wezel]['group']):
                    siec.nodes[wezel]['group'] = 'podharcmistrz'
                    siec.nodes[wezel]['color'] = '#0a5c0a'
                    nowy_phm += 1
            elif siec.nodes[wezel]['group'] == 'podharcmistrz' and wiek >= 21 and wartosc_polaczen > 1:
                prawdopodobienstwo3 = random.uniform(0, 1)
                if prawdopodobienstwo3 < prawdopodobienstwo_zmiana(wiek, stopien, siec.nodes[wezel]['group']):
                    siec.nodes[wezel]['group'] = 'harcmistrz'
                    siec.nodes[wezel]['color'] = '#ff0000'
                    nowy_hm += 1
            wezel += 1
    # Zmiana wieku
    for wezel in range(len(siec.nodes)):
        siec.nodes[wezel]['label'] += 1
        siec.nodes[wezel]['title'] = f"Wiek: {siec.nodes[wezel]['label']}"

    # Zebranie danych do wykresów
    liczba_harcerzy.append(h)
    liczba_przewodnikow.append(pwd)
    liczba_podharcmistrzow.append(phm)
    liczba_harcmistrzow.append(hm)
    liczba_kadry.append(pwd + phm + hm)

    lista_nowych_harcerzy.append(nowy_h)
    lista_nowych_przewodnikow.append(nowy_pwd)
    lista_nowych_podharcmistrzow.append(nowy_phm)
    lista_nowych_harcmistrzow.append(nowy_hm)

    liczba_zuchow.append(z)
    liczba_harcerzy_m.append(har_m)
    liczba_hs.append(hs)
    liczba_w.append(w)
    liczba_star.append(star)

    lista_usun.append(usun)
    relacje.append(len(siec.edges))
    #Zapisanie struktury sieci w danym roku
    siec.show(f"network_frame{rok+1}.html")


# Tworzenie wykresu wzrostu krawędzi
plt.plot(relacje, label='Liczba relacji', color='red')
plt.xlabel('Rok')
plt.ylabel('Liczba relacji')
plt.title('Wzrost liczby relacji')
plt.legend()
plt.grid()
plt.show()


# Tworzenie wykresu liczebności
plt.plot(liczba_harcerzy, label='Liczba harcerzy', color='yellow')
plt.plot(liczba_przewodnikow, label='Liczba przewodników', color='blue')
plt.plot(liczba_podharcmistrzow, label='Liczba podharcmistrzów', color='green')
plt.plot(liczba_harcmistrzow, label='Liczba harcmistrzów', color='red')
plt.plot(liczba_czlonkow, label='liczba czlonkow', color='black')
plt.xlabel('Rok')
plt.ylabel('Liczba członków')
plt.title('Wykres zmiany liczebności członków organizacji')
plt.legend()
plt.grid()
plt.show()

# Tworzenie wykresu wzrostu liczebności poszczególnych stanów
plt.plot(lista_nowych_harcerzy, label='Liczba harcerzy, którzy dołączyli do organizacji', color='yellow')
plt.plot(lista_nowych_przewodnikow, label='Liczba ukończonych prób przewodnikowskich', color='blue')
plt.plot(lista_nowych_podharcmistrzow, label='Liczba ukończonych prób podharcmistrzowskich', color='green')
plt.plot(lista_nowych_harcmistrzow, label='Liczba ukończonych prób harcmistrzowskich', color='red')
plt.xlabel('Rok')
plt.ylabel('Liczba członków')
plt.title('Wykres wzrostu')
plt.legend()
plt.grid()
plt.show()

# Tworzenie wykresu grup wiekowych w organizacji
plt.plot(liczba_zuchow, label='Liczba członków w wieku zuchowym', color='yellow')
plt.plot(liczba_harcerzy_m, label='Liczba czlonków w wieku harcerskim', color='blue')
plt.plot(liczba_hs, label='Liczba członków w wieku starszoharcerskim', color='green')
plt.plot(liczba_w, label='Liczba członków w wieku wędrowniczym', color='red')
plt.plot(liczba_star, label='Liczba członków w wieku starszyzny', color='black')
plt.xlabel('Rok')
plt.ylabel('Liczba członków')
plt.title('Wykres liczebności grup wiekowych')
plt.legend()
plt.grid()
plt.show()

# Tworzenie wykresu porównującego liczbę osób, które dołączyły i które opuściły organizacje
plt.plot(lista_usun, label='Liczba osób, które opuściły organizacje', color='red')
plt.plot(lista_nowych_harcerzy, label='Liczba osób, które wstąpiły do organizacji', color='green')
plt.xlabel('Rok')
plt.ylabel('Liczba osób')
plt.title('Porównanie liczby osób, które opuściły i dołączyły do organizacji')
plt.legend()
plt.grid()
plt.show()

# Tworzenie wykresu porównującego liczbę kadry i podopoiecznych
plt.plot(liczba_harcerzy, label='Liczba podpopiecznych', color='red')
plt.plot(liczba_kadry, label='Liczba członków kadry', color='green')
plt.xlabel('Rok')
plt.ylabel('Liczba osób')
plt.title('Porównanie liczby podopiecznych i liczby kadry')
plt.legend()
plt.grid()
plt.show()


