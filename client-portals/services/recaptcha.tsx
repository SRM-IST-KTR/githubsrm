import { load } from "recaptcha-v3";

export async function getRecaptchaToken(action: string) {
  const siteKey = "6Ldz6VcbAAAAANLyjRiKpGycGO74Jghb2jTgTRKk";
  const recaptcha = await load(siteKey);
  const token = await recaptcha.execute(action);

  return token;
}
