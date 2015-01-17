var dogeViewModel = {
  users: ko.observableArray([]),
  messages: ko.observableArray([]),
  transactions: ko.observableArray([]),
  walletTransactions: ko.observableArray([]),
  logLines: ko.observableArray([])
};

function User(name, balance) {
  this.name = name;
  this.balance = parseFloat(balance).toFixed(2);
};

function Message(name, message) {
  this.name = name;
  this.message = message;
};

function Transaction(from_name, to_name, amount) {
  this.fromName = from_name;
  this.toName = to_name;
  this.amount = parseFloat(amount).toFixed(2);
}

function WalletTransaction(name, is_deposit, amount) {
  this.name = name;
  this.type = is_deposit ? "deposit" : "withdrawl";
  this.amount = parseFloat(amount).toFixed(2);
}

function LogLine(line) {
  this.text = line;
}

window.setInterval(function() {
  $.ajax("/api/v1/user")
    .done(function(success) {
      users = _.map(success.objects, function(user_obj) {
        return new User(
          user_obj.user_name,
          user_obj.balance
        );
      });
      dogeViewModel.users(users);
    });
}, 10000);

window.setInterval(function() {
  $.ajax("/api/v1/message")
    .done(function(success) {
      messages = _.map(success.objects, function(message_obj) {
        return new Message(
          message_obj.user_name,
          message_obj.message
        );
      });
      dogeViewModel.messages(messages);
    });
}, 10000);

window.setInterval(function() {
  $.ajax("/api/v1/transaction")
    .done(function(success) {
      transactions = _.map(success.objects, function(transaction_obj) {
        return new Transaction(
          transaction_obj.to_user.user_name,
          transaction_obj.from_user.user_name,
          transaction_obj.amount
        );
      });
      dogeViewModel.transactions(transactions);
    });
}, 10000);

window.setInterval(function() {
  $.ajax("/api/v1/wallettransaction")
    .done(function(success) {
      transactions = _.map(success.objects, function(transaction_obj) {
        return new WalletTransaction(
          transaction_obj.user.user_name,
          transaction_obj.is_deposit,
          transaction_obj.amount
        );
      });
      dogeViewModel.walletTransactions(transactions);
    });
}, 10000);

window.setInterval(function() {
  $.ajax("/getlog")
    .done(function(success) {
      dogeViewModel.logLines(success.objects.reverse());
    });
}, 10000);
