# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B1` detalla el slice `B1` del caso de uso `CU001`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de los **tres slices básicos** del camino feliz (`B1`, `B2`, `B3`) del único caso de uso profundizado (`CU001`), más una HU de un slice de excepción representativo (`E1`, secuencia con formato inválido). El resto de los slices están **nombrados en el caso de uso** ([`casos-de-uso.md`](casos-de-uso.md)) y se detallarán como HU cuando algún TP posterior los necesite — no es obligación abrirlos todos ya, como aclara la propia guía del TP1.

---