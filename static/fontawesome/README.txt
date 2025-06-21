Zde budou uloženy soubory Font Awesome pro lokální načítání ikon. 

1. Stáhni si balíček Font Awesome Free (např. z https://fontawesome.com/download).
2. Zkopíruj obsah složky `css` a `webfonts` do této složky.
3. V base.html změň odkaz na CDN na lokální:
   <link rel="stylesheet" href="{% static 'fontawesome/css/all.min.css' %}">

Tím se ikony budou načítat rychleji a bez závislosti na internetu.
