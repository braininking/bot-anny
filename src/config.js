import "dotenv/config";

export const config = {
  apiId: Number(process.env.TELEGRAM_API_ID),
  apiHash: process.env.TELEGRAM_API_HASH,
  session: process.env.TELEGRAM_SESSION || "",
  targetChannel: process.env.TARGET_CHANNEL,
  sourceChannels: (process.env.SOURCE_CHANNELS || "")
    .split(",")
    .map(v => v.trim())
    .filter(Boolean),
  amazonTag: process.env.AMAZON_TAG || "ofertaradar03-20",
  magaluAffiliateId: process.env.MAGALU_AFFILIATE_ID || "magazineoneshotlink",
  kabumAwinId: process.env.KABUM_AWIN_ID || "23038"
};

if (!config.apiId || !config.apiHash) {
  throw new Error("TELEGRAM_API_ID e TELEGRAM_API_HASH são obrigatórios.");
}
if (!config.targetChannel) {
  throw new Error("TARGET_CHANNEL é obrigatório.");
}
if (!config.sourceChannels.length) {
  throw new Error("SOURCE_CHANNELS precisa ter pelo menos um canal.");
}
