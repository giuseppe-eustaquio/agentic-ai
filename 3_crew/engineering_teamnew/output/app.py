import gradio as gr
from accounts import Account, get_share_price

# Initialize the account with a user ID and initial deposit
account = Account(user_id="user1", initial_deposit=10000)

# Gradio UI functions
def deposit(amount):
    try:
        account.deposit(float(amount))
        return f"Deposit successful. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw(amount):
    try:
        account.withdraw(float(amount))
        return f"Withdrawal successful. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, int(quantity))
        return f"Bought {quantity} shares of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, int(quantity))
        return f"Sold {quantity} shares of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def get_portfolio():
    holdings = account.get_holdings()
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_loss()
    return f"Holdings: {holdings}\nPortfolio Value: {portfolio_value}\nProfit/Loss: {profit_loss}"

def get_transactions():
    transactions = account.get_transactions()
    return transactions

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Account Management")
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            amount_input = gr.Number(label="Amount")
            deposit_button = gr.Button("Deposit")
            withdraw_button = gr.Button("Withdraw")
        result_text = gr.Textbox(label="Result")
        
        deposit_button.click(deposit, inputs=amount_input, outputs=result_text)
        withdraw_button.click(withdraw, inputs=amount_input, outputs=result_text)
    
    with gr.Tab("Buy/Sell Shares"):
        with gr.Row():
            symbol_input = gr.Textbox(label="Symbol (e.g., AAPL, TSLA, GOOGL)")
            quantity_input = gr.Number(label="Quantity")
            buy_button = gr.Button("Buy")
            sell_button = gr.Button("Sell")
        result_text_shares = gr.Textbox(label="Result")
        
        buy_button.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=result_text_shares)
        sell_button.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=result_text_shares)
    
    with gr.Tab("Portfolio and Transactions"):
        portfolio_button = gr.Button("Get Portfolio")
        transactions_button = gr.Button("Get Transactions")
        portfolio_text = gr.Textbox(label="Portfolio")
        transactions_text = gr.JSON(label="Transactions")
        
        portfolio_button.click(get_portfolio, outputs=portfolio_text)
        transactions_button.click(get_transactions, outputs=transactions_text)

if __name__ == "__main__":
    demo.launch()