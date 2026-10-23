# Integración con Xray (Jira Cloud)

Cada test de Pytest está vinculado a su caso de prueba en Jira/Xray (proyecto `SCRUM`)
mediante el marker `@pytest.mark.xray("SCRUM-XX")`. Al ejecutar la regresión con el
plugin [`pytest-jira-xray`](https://github.com/walkIT-nl/pytest-jira-xray), los resultados
(PASS / FAIL) se publican en Xray y actualizan el estado de cada test.

## Mapeo de tests

| TC | Jira | Test Pytest |
|---|---|---|
| TC-001 | SCRUM-28 | `tests/integration/test_measurement_flow.py` |
| TC-002 | SCRUM-29 | `tests/integration/test_device_mode_flow.py` |
| TC-003 | SCRUM-30 | `tests/integration/test_firmware_update_flow.py` |
| TC-004 | SCRUM-31 | `tests/integration/test_firmware_update_failure.py` |
| TC-005 | SCRUM-32 | `tests/api/test_hydration_score_generation.py` |
| TC-006 | SCRUM-33 | `tests/api/test_recommendation_generation.py` |
| TC-007 | SCRUM-34 | `tests/api/test_anonymous_measurement.py` |
| TC-008 | SCRUM-35 | `tests/api/test_insufficient_volume_measurement.py` |
| TC-009 | SCRUM-36 | `tests/api/test_duplicate_measurement.py` |
| TC-010 | SCRUM-37 | `tests/integration/test_device_disconnect_mid_measurement.py` |
| TC-011 | SCRUM-38 | `tests/integration/test_buffered_measurement_upload.py` |
| TC-012 | SCRUM-39 | `tests/integration/test_backend_unavailable.py` |
| TC-013 | SCRUM-40 | `tests/api/test_invalid_api_response.py` |
| TC-014 | SCRUM-41 | `tests/api/test_wrong_user_association.py` |
| TC-015 | SCRUM-42 | `tests/api/test_clinically_implausible_measurement.py` (3 casos) |
| TC-016 | SCRUM-43 | `test_clinically_implausible_measurement[score_above_range / score_below_range]` |
| TC-017 | SCRUM-44 | `test_clinically_implausible_measurement[extreme_ph]` |

## Configuración

Credenciales: en Jira → Apps → Xray → Configuración global → **API Keys** se genera un
Client ID y un Client Secret. Se guardan en GitHub → Settings → Secrets and variables → Actions:

| Tipo | Nombre | Valor |
|---|---|---|
| Secret | `XRAY_CLIENT_ID` | Client ID de Xray |
| Secret | `XRAY_CLIENT_SECRET` | Client Secret de Xray |
| Variable (opcional) | `XRAY_API_BASE_URL` | `https://xray.cloud.getxray.app` por defecto; usar el endpoint regional (p. ej. `https://eu.xray.cloud.getxray.app`) si la autenticación falla |

Si los secrets no existen, el pipeline ejecuta los tests igualmente sin publicar en Xray.

## Ejecución

En CI cada ejecución del workflow crea una **Test Execution nueva** en Xray con los 17 resultados
(resumen: `Regresión automatizada - <rama> #<run>`, revisión: SHA del commit).

En local:

```bash
export XRAY_API_BASE_URL=https://xray.cloud.getxray.app
export XRAY_CLIENT_ID=...
export XRAY_CLIENT_SECRET=...

# Nueva Test Execution
pytest --jira-xray --cloud --client-secret-auth --allow-duplicate-ids

# Actualizar una Test Execution existente
pytest --jira-xray --cloud --client-secret-auth --allow-duplicate-ids --execution SCRUM-47

# Generar el informe Xray en un fichero sin publicarlo (útil para revisar el mapeo)
pytest --jira-xray --xraypath=xray-report.json --allow-duplicate-ids
```

`--allow-duplicate-ids` es necesario porque los tres casos del test parametrizado de
plausibilidad clínica reportan también a TC-015 (SCRUM-42).

## Suites por etiqueta (Smoke / Sanity / Regresión)

Los tests llevan markers de pytest (`@pytest.mark.smoke`, `@pytest.mark.sanity`) registrados en
`pytest.ini` con `--strict-markers`. Los Test de Xray llevan las mismas etiquetas en Jira
(`smoke`, `sanity`), de modo que se pueden filtrar también allí (p. ej. `labels = smoke`).

| Suite | Marker | Casos |
|---|---|---|
| Smoke Test | `smoke` | TC-001, TC-002, TC-003, TC-005, TC-006 |
| Sanity Test | `sanity` | TC-004, TC-008, TC-009, TC-012, TC-014, TC-015 (+ TC-016 y TC-017, mismo test parametrizado) |
| Regresión | — | Los 17 casos |

Ejecución local:

```bash
pytest -m smoke                 # o: make smoke   / ./run_qa.sh smoke
pytest -m sanity                # o: make sanity  / ./run_qa.sh sanity
pytest                          # regresión completa: make test / ./run_qa.sh
pytest -m "smoke or sanity"     # combinaciones
```

En GitHub Actions: **Actions → QA Regression Suite → Run workflow** y elegir la suite
(`regression`, `smoke` o `sanity`). Los push y pull requests ejecutan siempre la regresión completa.
La Test Execution creada en Xray indica la suite en el título, p. ej.
`Ejecución automatizada (Smoke Test) - main #12`.

Para mover un test de suite basta con cambiar su marker en el código y la etiqueta del Test en Jira.
