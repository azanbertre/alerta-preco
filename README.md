# Alerta Preço

Obs: Esse app foi desenvolvido com o objetivo de ser utilizado junto da aplicação [Join](https://play.google.com/store/apps/details?id=com.joaomgcd.join&hl=pt_BR). Entretanto é possivel utilizá-lo com uma api própria.

## Lojas disponíveis
Links com produtos nessas lojas irão funcionar
- [Amazon](https://www.amazon.com.br)
- [Americanas](https://www.americanas.com.br)
- [Submarino](https://www.submarino.com.br)
- [Magazine Luiza](https://www.magazineluiza.com.br)
- [Casas Bahia](https://www.casasbahia.com.br)
- [Extra](https://www.extra.com.br)

## Para rodar
Instalar as depedências
```bash
pip install -r requirements.txt
```
Rodando o script
```bash
python run.py
```

## Configuração
Arquivo `settings.json`
```
{
    "postUrl": "", // Resultados serão enviados para cá se o Join não estiver configurado
    "apiKey": "", // Key da api do Join
    // Lista com os produtos a serem verificados
    "products": [
        {
            "url": "", // Url da página do produto
            "price": 0 // Preço ideal (Alerta será enviado se o preço do produto for menor que este)
        },
    ],
    "interval": 0 // Intervalo para busca de valores em minutos  (mínimo um minuto)
}
```

## Sobre

O script irá verificar as páginas dos produtos definidos em `setting.json` à cada `interval` minutos. O resultado é enviado para o api do Join que aciona uma notificação em todos os dispositivos conectados ou à uma url de api própria.

### Exemplo de notificação:
![alt text](https://i.imgur.com/P0g9TTz.png)
