import { classifyAndConvert } from "./converters.js";

const URL_REGEX = /https?:\\/\\/[^\\s<>]+/gi;
const processed = new Set();

export function extractUrls(text) {
  return [...new Set((text.match(URL_REGEX) || []).map(u => u.replace(/[),.!?]+$/g, "")))];
}

export function processText(text) {
  const urls = extractUrls(text);
  if (!urls.length) return null;

  const converted = [];
  for (const url of urls) {
    const result = classifyAndConvert(url);

    // Regra de ouro: se houver qualquer loja não suportada,
    // a mensagem inteira é descartada.
    if (!result) return null;

    converted.push({ original: url, ...result });
  }

  let output = text;
  for (const item of converted) {
    output = output.split(item.original).join(item.url);
  }

  const fingerprint = converted.map(x => x.url).sort().join("|");
  if (processed.has(fingerprint)) return null;
  processed.add(fingerprint);

  // Evita crescimento infinito em processos de longa duração.
  if (processed.size > 5000) {
    const first = processed.values().next().value;
    processed.delete(first);
  }

  return { text: output, stores: converted.map(x => x.store) };
}
