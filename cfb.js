const http = require('http');
const https = require('https');
const url = require('url');
const { setTimeout } = require('timers/promises');

// ===== CONFIGURATION ===== //
const TARGET_URL = 'https://grim.ac/'; // CHANGE THIS
const REQUESTS_PER_SECOND = 50; // Adjust based on server capacity
const TEST_DURATION_MS = 30000; // 30 seconds
const MAX_CONCURRENT_REQUESTS = 20; // Simulate multiple users

// ===== USER AGENT ROTATION ===== //
const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/115.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
];

// ===== REFERER SPOOFING ===== //
const REFERERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.yahoo.com/',
    'https://www.facebook.com/',
    'https://www.reddit.com/',
    'https://twitter.com/',
    'https://www.linkedin.com/',
    'https://www.youtube.com/',
    'https://www.amazon.com/',
    'https://www.wikipedia.org/'
];

// ===== STATISTICS ===== //
let stats = {
    totalRequests: 0,
    success: 0,
    errors: 0,
    blockedByCloudflare: 0,
    startTime: Date.now()
};

// ===== REQUEST FUNCTION ===== //
async function sendRequest() {
    const parsedUrl = url.parse(TARGET_URL);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;

    const headers = {
        'User-Agent': USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': REFERERS[Math.floor(Math.random() * REFERERS.length)],
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache'
    };

    const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: parsedUrl.path,
        method: 'GET',
        headers: headers,
        timeout: 5000
    };

    return new Promise((resolve) => {
        const req = protocol.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                stats.totalRequests++;
                if (res.statusCode === 200) {
                    stats.success++;
                    if (data.includes('Cloudflare') || res.headers['server']?.includes('cloudflare')) {
                        stats.blockedByCloudflare++;
                    }
                } else {
                    stats.errors++;
                }
                resolve();
            });
        });

        req.on('error', (err) => {
            stats.errors++;
            resolve();
        });

        req.end();
    });
}

// ===== MAIN LOAD TEST ===== //
async function runLoadTest() {
    console.log(`🚀 Starting Advanced Load Test on: ${TARGET_URL}`);
    console.log(`⚡ Requests/sec: ${REQUESTS_PER_SECOND} | Duration: ${TEST_DURATION_MS / 1000}s`);

    const startTime = Date.now();
    const endTime = startTime + TEST_DURATION_MS;

    while (Date.now() < endTime) {
        const requests = [];
        for (let i = 0; i < MAX_CONCURRENT_REQUESTS; i++) {
            requests.push(sendRequest());
        }
        await Promise.all(requests);
        await setTimeout(1000 / REQUESTS_PER_SECOND); // Rate limiting
    }

    // Print results
    console.log('\n📊 Test Results:');
    console.log('================');
    console.log(`✅ Successful Requests: ${stats.success}`);
    console.log(`❌ Failed Requests: ${stats.errors}`);
    console.log(`🛡️ Cloudflare Blocks: ${stats.blockedByCloudflare}`);
    console.log(`⏱️ Total Time: ${(Date.now() - startTime) / 1000}s`);
}

runLoadTest().catch(console.error);