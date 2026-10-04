import { config } from "./config.js";

export function isAmazon(url) {
  return /amazon\\.com\\.br/i.test(url);
}

export function isMagalu(url) {
  return /(magazineluiza\\.com\\.br|magalu\\.com\\.br)/i.test(url);
}

export function isKabum(url) {
  return /kabum\\.com\\.br/i.test(url);
}

export function convertAmazon(url) {
  const parsed = new URL(url);
  parsed.searchParams.set("tag", config.amazonTag);
  return parsed.toString();
}

export function convertMagalu(url) {
  // Mantido isolado porque o formato final do deeplink Magalu depende
  // da estrutura/credencial do programa de afiliados.
  return url;
}

export function convertKabum(url) {
  // Estrutura solicitada: https://awin1.com + URL do produto.
  // O ID do anunciante fica configurável para futura validação Awin.
  return "https://awin1.com" + url;
}

export function classifyAndConvert(url) {
  if (isAmazon(url)) return { store: "amazon", url: convertAmazon(url) };
  if (isMagalu(url)) return { store: "magalu", url: convertMagalu(url) };
  if (isKabum(url)) return { store: "kabum", url: convertKabum(url) };
  return null;
}
