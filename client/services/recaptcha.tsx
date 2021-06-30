import { load } from "recaptcha-v3";

export async function getRecaptchaToken(action: string) {
  const siteKey = process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY;
  const recaptcha = await load(siteKey);
  const token = await recaptcha.execute(action);

  return token;
}
