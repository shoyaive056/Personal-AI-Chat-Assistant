// Small helper so message IDs aren't generated ad-hoc in multiple places.
export function generateId() {
  return crypto.randomUUID();
}
