# Vytvoření databáze MySQL pro projekt hypoteky

1. Otevřete terminál a spusťte MySQL klienta:
   
   ```sh
   mysql -u root -p
   ```
   (Zadejte heslo k MySQL)

2. Vytvořte databázi:
   ```sql
   CREATE DATABASE hypoteky CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci;
   ```

3. (Volitelné) Vytvořte uživatele a přidělte mu práva:
   ```sql
   CREATE USER 'hypoteky_user'@'localhost' IDENTIFIED BY 'silneheslo';
   GRANT ALL PRIVILEGES ON hypoteky.* TO 'hypoteky_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Upravte `settings.py`:
   - `NAME`: hypoteky
   - `USER`: hypoteky_user (nebo root)
   - `PASSWORD`: silneheslo (nebo vaše root heslo)

5. Proveďte migrace:
   ```sh
   source venv/bin/activate
   python manage.py migrate
   ```

Pokud narazíte na chybu s mysqlclient, ujistěte se, že máte nainstalované potřebné knihovny:
```sh
brew install mysql
pip install mysqlclient
```
