import websocket
import ast

prev = {};

def on_message(ws, message):
    m = ast.literal_eval(message);
    
    kind = m.get("type");
    
    if kind == "trade":
        ticker = m.get("data")[0].get("s");
        price = m.get("data")[0].get("p");
        if not prev.get(ticker):
            prev[ticker] = price;

        else:
            diff = price - prev.get(ticker);
            if diff > 0:
                print("{} : +{}".format(ticker, diff));
            else:
                print("{} : {}".format(ticker, diff));
            prev[ticker] = price;


def on_error(ws, error):
    print(error);

def on_close(ws):
    print("### Terminated ###");

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}');
    ws.send('{"type":"subscribe","symbol":"AMZN"}');

if __name__ == "__main__":
    websocket.enableTrace(True);
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=brlsu37rh5re8ma1ndkg", on_message = on_message, on_error = on_error, on_close = on_close);
    ws.on_open = on_open;
    ws.run_forever();