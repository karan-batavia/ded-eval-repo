# Expected classification

Every row is a variable the scanner should surface. `Rule` names the rule that decides it.

Nothing in this repo carries a suppression signal — no `test` / `mock` / `sample` / `demo` / `fixture`
in any path, class name, or comment. That is deliberate. Rule 3 suppresses on those tokens, so a repo
that looked like a fixture would score `None` everywhere and prove nothing.

## analytics/warehouse_export.py — SQL column names (PROD-264)

| Variable | Expected tag | Rule |
|---|---|---|
| `"member_id"` | AccountData.AccountID | 3a |
| `"email_address"` | ContactData.EmailAddress | 3a |
| `"phone_number"` | ContactData.PhoneNumber | 3a |
| `"billing_address"` | ContactData.Address | 3a |
| `"date_of_birth"` | PersonalIdentification.DateofBirth | 3a |
| `"created_at"` | None | 4 — generic attribute |
| `"member_profile"` | None | 3a — table name, names no field |
| `"Sending export summary to member"` | None | 3a — prose |
| `columns`, `column`, `column_lower`, `select_items`, `sensitive_columns`, `table_name` | None | 3a — carriers |
| `ROW_FMT` (`"%s \| %s"`) | None | 3 — format pattern, holds no data |
| `PHONE_RE` (`r"^\d{3}-\d{4}$"`) | None | 3 — regex pattern, holds no data |
| `spark`, `app_name`, `encryption_key`, `WAREHOUSE_JAR_PATH`, `MASK_CLASS`, `RETRY_LIMIT`, `attempt`, `err` | None | 3 |

`ROW_FMT` and `PHONE_RE` are the guard on Rule 3's format-string clause. That clause was narrowed so it
stops covering a field name inside an f-string. These two rows prove the narrowing did not also stop it
covering a real pattern. If either comes back tagged, the narrowing went too far.

## api/employee_sync.py — dict keys (PROD-276 case 1)

| Variable | Expected tag | Rule |
|---|---|---|
| `'firstName'` | PersonalIdentification.FirstName | 3a |
| `'lastName'` | PersonalIdentification.LastName | 3a |
| `'mobile'` | ContactData.PhoneNumber | 3a |
| `'home_address'` | ContactData.Address | 3a |
| `'departmentCode'` | None | 4 — generic attribute |
| `'companyId'` | None | 3 — organisation identifier |
| `full_name` | PersonalIdentification.FullName | 1 — holds the joined name at runtime |
| `contact` | ContactData.PhoneNumber | 1 — holds the mobile value |
| `home` | ContactData.Address | 1 — holds the address value |
| `dept`, `org`, `entry` | None | 4 / 3 |

The three holder rows are the reverse guard. The literals above them test that a *name* gets tagged;
these test that a variable actually holding the value still gets tagged too. A prompt change that
over-corrects toward names could drop them.

## src/main/java/com/acme/ledger/LedgerColumns.java — constants

The two `"email_address"` constants hold the same string and must get opposite answers.
Only the use site separates them.

| Variable | Expected tag | Rule |
|---|---|---|
| `COL_EMAIL` → `rs.getString(COL_EMAIL)` | ContactData.EmailAddress | 3a |
| `COL_TAX_ID` → `rs.getString(COL_TAX_ID)` | NationalIdentificationNumbers.TaxpayerIdentificationNumber | 3a |
| `CSS_EMAIL` → `el.addClass(CSS_EMAIL)` | None | 3a — names no field |
| `METRIC_NAME` → `metrics.increment(METRIC_NAME)` | None | 3a — names a counter |
| `DEFAULT_SENDER` | None | 3 — hardcoded value |

## src/main/java/com/acme/ledger/ContactMapping.java — mappings + query builder (PROD-276 case 2)

| Variable | Expected tag | Rule |
|---|---|---|
| `"meta.createdBy.firstName"` | PersonalIdentification.FirstName | 3a |
| `"meta.createdBy.lastName"` | PersonalIdentification.LastName | 3a |
| `"home_address"` | ContactData.Address | 3a |
| `"date_of_birth"` | PersonalIdentification.DateofBirth | 3a |
| `"meta.updated"`, `"workflowPhase"`, `"unit_count"`, `"residents"`, `"buildings"` | None | 3a / 4 |

## app/src/main/java/com/acme/profile/ProfileScreen.kt — UI controls (PROD-278)

| Variable | Expected tag | Rule |
|---|---|---|
| `userName` | AccountData.AccountName | 4.5 |
| `dobField` | PersonalIdentification.DateofBirth | 4.5 — name only, no assignment |
| `phoneField` | ContactData.PhoneNumber | 4.5 — name only, no assignment |
| `emailLabel` | None | 4.5 — fixed caption |
| `screenTitle`, `retryCount` | None | 3 |

## Reading the run

- Any row expecting a tag that comes back `None` is a false negative — the rule did not fire.
- Any row expecting `None` that comes back tagged is a false positive — the rule fired too wide.
- The second column of each `None` row says which rule is meant to hold it back. If a `None` row
  flips, that rule is the one to look at.
