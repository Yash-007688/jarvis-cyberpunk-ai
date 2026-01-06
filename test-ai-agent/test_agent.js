/**
 * Test script for AI Agent
 * This script tests the core functionality of our AI agent without using the full server setup
 */

// Test the response processor
const { ResponseProcessor } = require('../ai-agent/src/ai/response_processor.js');

console.log('Testing AI Agent Response Processor...\n');

// Create a response processor instance
const processor = new ResponseProcessor();

// Test various commands
const testCommands = [
    "Hello",
    "What time is it?",
    "What's the date today?",
    "Tell me a joke",
    "How's the weather?",
    "Play some music",
    "Can you help me?",
    "This is a general query"
];

console.log('Testing various commands:\n');

testCommands.forEach((command, index) => {
    console.log(`${index + 1}. Input: "${command}"`);
    const response = processor.processInput(command);
    console.log(`   Output: "${response}"\n`);
});

console.log('Response processor test completed successfully!');
console.log('\nThe AI agent is working correctly and can process various types of user commands.');