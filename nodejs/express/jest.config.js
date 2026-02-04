module.exports = {
  testEnvironment: 'node',
  coveragePathIgnorePatterns: ['/node_modules/'],
  testMatch: ['**/__tests__/**/*.test.js'],
  collectCoverageFrom: [
    'routers/**/*.js',
    '!routers/**/elevenlabs_sample.js', // Skip external API integration
  ],
};
