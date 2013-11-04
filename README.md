Sports tracker with achievements
================================

Kilka informacji o projekcie
----------------------------

### Paginacja

Zamiast za każdym razem robić copypastę z dokumentacji Django z tymi wszyskimi
try...except, wygeneruj stronę paginatora korzystając z funkcji
`get_page()` z `app.shared.helpers`

Aby wsadzić nawigację paginacji do templatki skorzystaj ze snippeta:

```
{% include "snippets/pagination.html" %}
```

**Uwaga!** Strona paginacji musi zostać przekazana do templatki jako `page`
