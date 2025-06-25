export function isJwtValid(token: string): boolean {
  if (!token) return false
  try {
    const [, payload] = token.split('.')
    const { exp } = JSON.parse(atob(payload))
    return Date.now() < exp * 1000
  } catch {
    return false
  }
}
