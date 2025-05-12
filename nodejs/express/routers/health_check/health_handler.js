const express = require('express');
const os = require('os');

const router = express.Router();

/**
 * @swagger
 * /health-check:
 *   get:
 *     tags:
 *       - Health
 *     summary: Health check endpoint
 *     description: Returns the health status of the API
 *     responses:
 *       200:
 *         description: A successful response
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                   example: OK
 *                 version:
 *                   type: string
 *                   example: 0.0.1
 *                 hostname:
 *                   type: string
 *                   example: hostname
 */
router.get('/health-check', (req, res) => {
  return res.status(200).json({
    message: 'OK',
    version: '0.0.1',
    hostname: os.hostname()
  });
});

module.exports = router;
