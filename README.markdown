[![travis](https://api.travis-ci.org/v0y/sport-tracker-with-acziwments.svg)](https://travis-ci.org/v0y/sport-tracker-with-acziwments)

Sports tracker with achievements
================================

Zaczynamy zabawę!
-----------------

1. Zainstaluj [virtualenv](https://pypi.python.org/pypi/virtualenv), utwórz
   virtualenva, aktywuj virtualenva, przejdź do katalogu, gdzie chcesz mieć
   projekt

1. `git clone git@github.com:v0y/sport-tracker-with-acziwments.git`

1. Przejdź do folderu zassanego projektu:
   ```sh
   cd sport-tracker-with-acziwments
   ```

1. Zainstaluj fabrica:
   ```sh
   pip install fabric
   ```

1. Zainstaluj Node.js:
   ```sh
   curl http://nodejs.org/dist/node-latest.tar.gz | tar xvz
   cd node-v*
   ./configure --prefix=$VIRTUAL_ENV
   make install
   ```

1. Zainstaluj npm:
   ```sh
   curl -L https://npmjs.org/install.sh | sh
   ```

1. Zainstaluj Bowera, uglify-js i uglifycss:
   ```sh
   sudo npm install bower uglify-js uglifycss
   ```

1. Zainstaluj zależności:
   ```sh
   fab install_requirements
   ```

1. Utwórz usera MySQL i bazę danych:
   ```sh
   fab create_database_role
   fab create_database
   ```

1. Odpal serwer:
   ```
   ./manage.py runserver
   ```


Kilka informacji o projekcie - kod
----------------------------------

### Paginacja

Zamiast za każdym razem robić copypastę z dokumentacji Django z tymi wszyskimi
try...except, wygeneruj stronę paginatora korzystając z funkcji
[`get_page()`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/helpers.html#shared.helpers.get_page) z `app.shared.helpers`

Aby wsadzić nawigację paginacji do templatki skorzystaj ze snippeta:

```django
{% include "snippets/pagination.html" %}
```

**Uwaga!** Strona paginacji musi zostać przekazana do templatki jako `page`


### Formularze

Snippety formularzy znajdują się w folderze `snippets`, więc inkludujemy je w
sposób:

```django
{% include "snippets/[nazwa snippeta]" %}
```

*   `form_vertical.html` - snippet całego formularza, łącznie z html-ową
    otoczką w postaci tagów `<form>` i podobnych. Pola ustawione jedno pod
    drugim. Obiekt formularza musi być przekazany jako `form`, formularz musi
    mieć w `Meta` podany tytuł (`name`) i treść tekstu buttona (`button_text`).

    Przykład:
    ```python
    class Meta:
        name = u"Logowanie"
        button_text = u"Zaloguj się"
    ```

*   `form_vertical_non_complex.html` - snippet formularza bez całej html-owej
    otoczki, więc sam musisz zadbać o `<form>`, `<fieldset>`, `<button>` i
    inne gówna. Zawiera wszystkie pola ułożone jedno pod drugim, komunikaty
    błędów i takie tam.

Do tego możesz sobie zerknąć, jakie inne snippety siedzą w folderze
`shared/templates/snippets`. Znajdziesz tam takie głupoty, jak snippet
komunikatu błędu w formie, przycisku formularza czy inne.

Jeśli jakieś mniej typowe pole Twojego formularza zostanie wyświetlone jako zły
typ, sprawdź, czy nie trzeba dopisać jego typu do tagu [`field_type()`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/templatetags/shared_filters.html#shared.templatetags.shared_filters.field_type)


### Wysyłanie maili

Aby wysłać maila wystarczy, że wywołasz funkcję [`simple_send_email()`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/helpers.html#shared.helpers.simple_send_email).


### Filtry

* [`I_dont_want_None()`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/templatetags/shared_filters.html#shared.templatetags.shared_filters.I_dont_want_None) -
  jeśli w templatce wyświetlasz jakąś zmienną, która może okazać się `None`,
  przefiltruj ją tym filtrem. Zamiast `Nona` dostaniesz pusty string.

* [`is_active_tab()`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/templatetags/shared_tags.html#shared.templatetags.shared_tags.is_active_tab) -
  filtrujesz nim `request`, jako parametr podajesz nazwę lub poszątkowy
  fragment urla (pamiętaj o początkowym slaszu!), on w całej swojej
  wdzięczności zwraca string `active`, jeśli właśnie znajdujemy się pod
  podanym urlem.


### Mixiny modeli

#### `app.shared.models`

* [`CreatedAtMixin`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.CreatedAtMixin) -
  Czas utworzenia, czyli `DateTimeField` z `auto_now_add=True`
* [`NameMixin`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.NameMixin) -
  Nazwa. Posiada metodę `__unicode__` zwracającą nazwę jako unicode.
* [`RelatedDateMixin`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.RelatedDateMixin) -
  Czyli zwykły `DateTimeField`
* [`SHA1TokenMixin`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.SHA1TokenMixin) -
  Token sha1, jeśli niepodany tworzy się z aktualnego przy zapisie czasu.
  Posiada metodę [`get_activation_link`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.SHA1TokenMixin.get_activation_link)
  pobierającą link z danym tokenem.
* [`SlugMixin`](http://sports-tracker-with-achievements.readthedocs.org/en/latest/static/modules/shared/models.html#shared.models.SlugMixin) -
  Slug. Jeśli niepodany, tworzy się z pola `name`.


Kilka informacji o projekcie - frontend
---------------------------------------

### Kolory

Schemat kolorów do użycia w kolorowych miejscach typu wykresy został
zaczerpnięty z [colourlovers.com](http://www.colourlovers.com/business/trends/branding/7880/Papeterie_Haute-Ville_Logo)

![kolory](docs/colors.png)


### Ikony

Nie używaj bootstrapowych [Glyphicons](http://getbootstrap.com/components/#glyphicons),
zamiast tegu użyj [Font Awesome 4](http://fontawesome.io/).


Narzędzia
---------

### Fabric

Aby sprawdzić dostępne polecenia fabrica odpal `fab --list` z głównego katalogu
projektu


### Less

W projekcie do pisania styli używany jest [less](http://lesscss.org).

Plików nie trzeba kompilować, wrzucamy je z użyciem django compressora, np:

```django
{% load compress %}

{% compress css %}
    <link rel="stylesheet" media="screen" href="{% static 'css/style.less' %}" type="text/less">
{% endcompress %}
```


### CSS

Zewnętrzne CSS-y powinny:

* być wrzucane do katalogu `app/shared/static/css` lub
  `app/shared/static/bootstrap/css` (jeśli dotyczą bootstrapa, np.
  "bootarap-cośtam.min.css"), chyba, że są szczególne dla jakiejś aplikacji -
  wtedy do statyków tej apki
* minimalizowane za pomocą [uglifycss](https://github.com/fmarcia/UglifyCSS) z
  parametrami `--cute-comments`, na przykład:
  ```
  uglifycss --cute-comments style.css > style.min.css
  ```
* po skompresowaniu zapisane z rozszerzeniem `*.min.css`. Nieskompresowany plik
  nie powinien się znaleźć w repo.

### JS

Zewnętrze biblioteki/skrypty js powinny:

* być wrzucane do katalogu `app/shared/static/js` lub
  `app/shared/static/bootstrap/js` (jeśli dotyczą bootstrapa, np.
  "bootarap-cośtam.min.js"), chyba, że są szczególne dla jakiejś aplikacji -
  wtedy do statyków tej apki
* minimalizowane za pomocą [`uglifyjs2`](https://github.com/mishoo/UglifyJS2) z
  parametrami `-c --preamble`, na przykład:
  ```
  uglifyjs script.js -o script.min.js -c --preamble
  ```
  Jeśli parametr `--preamble` uniemożliwi kompresję, należy skompresować plik
  bez niego, ale ręcznie przekleić nagłówek (ten komentarz z licencją, autorem,
  itp.) do pliku skompresowanego
* po skompresowaniu zapisane z rozszerzeniem `*.min.js`. Nieskompresowany plik
  nie powinien się znaleźć w repo.


### CoffeeScript

Plików nie trzeba kompilować, wrzucamy je z użyciem django compressora, np:

```django
{% load compress %}

{% compress js %}
    <script src="{% static 'js/map_handler.coffee' %}" type="text/coffeescript"></script>
{% endcompress %}
```


Zasady
------

### Urle

Ścieżki urli powinny wygladać mniej więcej tak:

```
/obiekt/add
/obiekt/edit
/obiekt/edit/identyfikator
/obiekt/show/identyfikator (jeśli tylko jeden typ widoku)
/obiekt/show/[list|chart|detail]/identyfikator
```

`identyfikator` - id lub slug

Gdy brak identyfikatora powinien zostać wyświetlony zasób dla zalogowanego
usera
