import { TelegramClient, Api } from "telegram";
import { StringSession } from "telegram/sessions/index.js";
import { NewMessage } from "telegram/events/index.js";
import input from "input";
import { config } from "./config.js";
import { processText } from "./processor.js";

const session = new StringSession(config.session);
const client = new TelegramClient(session, config.apiId, config.apiHash, {
  connectionRetries: 10
});

async function main() {
  await client.start({
    phoneNumber: async () => input.text("Número do Telegram: "),
    password: async () => input.text("Senha 2FA: "),
    phoneCode: async () => input.text("Código recebido no Telegram: "),
    onError: err => console.error("Telegram:", err)
  });

  console.log("Telegram conectado.");
  console.log("SESSION:", client.session.save());

  client.addEventHandler(async event => {
    try {
      const message = event.message;
      const text = message?.message || "";
      if (!text) return;

      const result = processText(text);
      if (!result) return;

      await client.sendMessage(config.targetChannel, {
        message: result.text
      });

      console.log("Oferta publicada:", result.stores.join(", "));
    } catch (error) {
      console.error("Erro ao processar mensagem:", error);
    }
  }, new NewMessage({ chats: config.sourceChannels }));

  console.log("Monitorando:", config.sourceChannels.join(", "));
  console.log("Destino:", config.targetChannel);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
