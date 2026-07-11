# LibraSys \u2014 \u0644\u064a\u0628\u0631\u0627\u0633\u064a\u0633

A modern, bilingual (English / Arabic) desktop library management system built with **Python** and **PyQt5**.

\u0646\u0638\u0627\u0645 \u0633\u0637\u062d\u064a \u062d\u062f\u064a\u062b \u062b\u0646\u0627\u0626\u064a \u0627\u0644\u0644\u063a\u0629 (\u0639\u0631\u0628\u064a / \u0625\u0646\u062c\u0644\u064a\u0632\u064a) \u0644\u0625\u062f\u0627\u0631\u0629 \u0627\u0644\u0645\u0643\u062a\u0628\u0627\u062a\u060c \u0645\u0628\u0646\u064a \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 **Python** \u0648 **PyQt5**.

---

## \u2728 Features

- **Full bilingual UI** \u2014 switch between English (LTR) and Arabic (RTL) live, no restart required. Layout, alignment and reading direction all flip automatically.
- **Dashboard** \u2014 KPI cards, a books-by-category bar chart, an availability donut chart, recent activity, and overdue alerts \u2014 all custom-painted with `QPainter` (no extra chart library needed).
- **Books catalog** \u2014 add / edit / delete, search, filter by category, CSV export, low-stock highlighting.
- **Members directory** \u2014 add / edit / delete, search, auto-generated member codes, membership types & status.
- **Borrow & Return** \u2014 issue loans with a configurable due date, track active loans, automatic overdue detection and fine calculation, one-click returns.
- **Reports** \u2014 Most Borrowed Books, Overdue Members, Full Inventory, Members List \u2014 each exportable to **CSV** or a formatted **PDF** (via `QPrinter`, bilingual layout aware).
- **Settings** \u2014 language, light/dark theme, library branding (name shown in the sidebar), configurable fine-per-day & loan period, password change, database backup/restore.
- **Authentication** \u2014 a simple login screen backed by a salted PBKDF2 password hash.
- **Data integrity guards** \u2014 you can't delete a book or member that still has items on loan; total-copy edits correctly reconcile against active loans.
- **Modern visual identity** \u2014 a deliberate "reading room" palette (deep emerald + brass/gold accents on warm paper tones, with a matching dark mode) instead of a generic default theme.

---

## \U0001F5C2\uFE0F Project structure

```
library_manager/
\u251c\u2500\u2500 main.py                  # entry point
\u251c\u2500\u2500 main_window.py            # sidebar + top bar + page container
\u251c\u2500\u2500 requirements.txt
\u251c\u2500\u2500 core/
\u2502   \u251c\u2500\u2500 database.py           # SQLite persistence layer (all queries live here)
\u2502   \u251c\u2500\u2500 translations.py       # EN/AR string table + LanguageManager
\u2502   \u251c\u2500\u2500 styles.py             # QSS theme builder (light & dark palettes)
\u2502   \u2514\u2500\u2500 helpers.py            # password hashing, date/fine math
\u251c\u2500\u2500 widgets/
\u2502   \u251c\u2500\u2500 sidebar.py            # left navigation
\u2502   \u251c\u2500\u2500 stat_card.py          # dashboard KPI card
\u2502   \u2514\u2500\u2500 charts.py             # dependency-free bar & donut charts
\u251c\u2500\u2500 dialogs/
\u2502   \u251c\u2500\u2500 login_dialog.py
\u2502   \u251c\u2500\u2500 book_dialog.py
\u2502   \u2514\u2500\u2500 member_dialog.py
\u2514\u2500\u2500 pages/
    \u251c\u2500\u2500 dashboard_page.py
    \u251c\u2500\u2500 books_page.py
    \u251c\u2500\u2500 members_page.py
    \u251c\u2500\u2500 borrow_page.py
    \u251c\u2500\u2500 reports_page.py
    \u2514\u2500\u2500 settings_page.py
```

The database file (`librasys.db`) and its seed data (a few sample books, members and loans) are created automatically next to `main.py` the first time you run the app.

---

## \u25B6\uFE0F Getting started

**1. Install dependencies** (Python 3.8+ recommended):

```bash
pip install -r requirements.txt
```

**2. Run the app:**

```bash
python main.py
```

**3. Sign in** with the default admin account:

```
Username: admin
Password: admin123
```

You can change this password from **Settings \u2192 Account & Security** once logged in.

### \u0627\u0644\u062a\u0634\u063a\u064a\u0644

1. \u062b\u0628\u062a \u0627\u0644\u0645\u062a\u0637\u0644\u0628\u0627\u062a: `pip install -r requirements.txt`
2. \u0634\u063a\u0651\u0644 \u0627\u0644\u0628\u0631\u0646\u0627\u0645\u062c: `python main.py`
3. \u0633\u062c\u0651\u0644 \u0627\u0644\u062f\u062e\u0648\u0644 \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 `admin` / `admin123` \u062b\u0645 \u063a\u064a\u0651\u0631\u0647\u0627 \u0645\u0646 \u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a.

---

## \U0001F3A8 Customizing the look

All colors live in `core/styles.py` as two plain dictionaries, `LIGHT` and `DARK`. Change any hex value there (primary color, accent, backgrounds, etc.) and every screen updates automatically \u2014 there's no styling duplicated across files.

The library name shown in the sidebar, the currency-less fine amount, and the default loan period are all editable from **Settings** without touching code.

## \U0001F310 Adding more languages

Everything text-facing goes through `lang.tr("some_key")`, backed by the `TRANSLATIONS` dictionary in `core/translations.py`. To add a third language you would extend each entry with a new language code and add a matching option in `LanguageManager`/Settings \u2014 no other file needs to change.

## \U0001F5C3\uFE0F Notes & known simplifications

- Deleting a book or a member also removes their borrow history (the confirmation dialogs say so); items currently on loan must be returned first \u2014 deletion is blocked in that case.
- The dashboard charts and PDF report tables render left-to-right regardless of the active language, which is standard practice for data visualizations even inside right-to-left interfaces.
- The bundled data is a local SQLite file, so **Backup Database** (Settings \u2192 Data Management) is the recommended way to keep a copy before major changes.

---

Built with \u2764\uFE0F using Python & PyQt5.
