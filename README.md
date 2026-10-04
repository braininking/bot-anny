# Telegram Forwarder Affiliate

Robô de monitoramento e tratamento de ofertas para Telegram.

## Lojas suportadas nesta primeira versão

- Amazon: substitui o parâmetro tag pelo ID configurado.
- Magalu: conversor isolado para receber a estrutura final do programa.
- KaBuM!: monta https://awin1.com + URL do produto.

Shopee, Mercado Livre e qualquer outra loja são descartados por enquanto.

## Configuração

1. Crie um app no Telegram para obter API ID e API HASH.
2. Copie .env.example para .env.
3. Informe os canais fonte em SOURCE_CHANNELS separados por vírgula.
4. Informe TARGET_CHANNEL.
5. Na primeira execução, faça login com a conta que terá acesso aos canais e permissão de publicação no canal destino.
6. Copie a SESSION exibida no terminal para TELEGRAM_SESSION para as próximas execuções.

## Segurança

Nunca publique .env ou a sessão do Telegram no Git.
