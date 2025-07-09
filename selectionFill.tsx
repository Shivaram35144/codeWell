async fillInputInSection(sectionLabel: string, fieldLabel: string, value: string): Promise<void> {
  const input = this.page.locator(`
    //*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(sectionLabel)}')]
      /ancestor::*[1]
        //input[
          contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
          contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
          contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
          contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}')
        ]
  `).first();

  await input.waitFor({ state: 'visible' });
  await input.fill(value);
}


async fillInputInSection(sectionLabel: string, fieldLabel: string, value: string): Promise<void> {
  const section = this.page.locator(`
    //*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(sectionLabel)}')]
  `).first();

  // Find the closest parent container (can be a div, section, td, etc.)
  const container = section.locator('xpath=ancestor::*[self::div or self::section or self::td or self::tr][1]');

  const input = container.locator(`
    .//input[
      contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
      contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
      contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}') or
      contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '${this.toXPathSafe(fieldLabel)}')
    ]
  `).first();

  await input.waitFor({ state: 'visible' });
  await input.fill(value);
}
