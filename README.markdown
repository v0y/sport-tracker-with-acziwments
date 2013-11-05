Sports tracker with achievements
================================

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
  filtrujesz nim `request`, jako parametr podajesz nazwę urla, on w całej
  swojej wdzięczności zwraca string `active`, jeśli właśnie znajdujemy się pod
  podanym urlem.


Kilka informacji o projekcie - frontend
---------------------------------------

### Kolory

Schemat kolorów do użycia w kolorowych miejscach typu wykresy został
zaczerpnięty z [colourlovers.com](http://www.colourlovers.com/business/trends/branding/7880/Papeterie_Haute-Ville_Logo)

![kolory](docs/colors.png)
