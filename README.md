# README #

### VIRTUALENV ###

* korzystamy z virtualenv
* aby utrzymać jedno wspólne środowisko trackujemy plik requirements.txt który jest outputem dla polecenia pip freeze odpalonego po wejściu do środowiska
* aby dociągnąć wszystkie paczki z pliku requirements.txt:
* * wchodzimy do środowiska poleceniem source sciezka_do_folderu_ze_srodowiskiem/bin/activate
* * wywoulujemy pip install -r requirements.txt
* * jeśli zmieniamy jakoś środowisko (dodajemy/usuwamy jakąś paczkę), wykonajmy również polecenie pip freeze > requirements.txt

* warto korzystać też z mkvirtualenv

* Póki co mamy tylko django tak na dobry start. 