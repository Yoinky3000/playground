export {};

const api = "https://discordapp.com/api/v9/entitlements/gift-codes/";

const wait = 2500

function generateRandomString() {
	const characters =
		"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	const length = 16;

	let randomString = "";
	for (let i = 0; i < length; i++) {
		const randomIndex = Math.floor(Math.random() * characters.length);
		randomString += characters.charAt(randomIndex);
	}

	return randomString;
}

async function tryCode(code: string) {
	const link = api + code;
	const res = await fetch(link);
	if (res.status == 429) {
		// @ts-ignore
		const { retry_after } = await res.json();
		console.log(`Rate Limited, wait for ${retry_after}`);
		await new Promise((res) => {
			setTimeout(res, retry_after * 1000);
		});
		return tryCode(code);
	}
	return res.status;
}

let tried = 0,
	valid = 0,
	invalid = 0;

(async () => {
	while (true) {
		const code = generateRandomString();
		const res = await tryCode(code);
		tried++;
		if (res !== 200) {
			invalid++;
		} else valid++;
		console.log(
			code +
				": " +
				res +
				` - Total: ${tried}, Valid: ${valid}, Invalid: ${invalid}`
		);
		await new Promise((res) => {
			setTimeout(res, wait);
		});
	}
})();
