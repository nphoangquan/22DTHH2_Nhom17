function greetUser(name) {
    const message = `Hello, ${name}! Welcome to our project. We are group 17`;
    return message;
}

function sayGoodbye(name) {
    return `Goodbye, ${name}! See you again.`;
}

console.log(sayGoodbye("Developer"));

module.exports = { greetUser, sayGoodbye };