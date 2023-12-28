# Ai Support Summary

This project aims at providing an API endpoint for answering questions from a CSV file.
Assumes that you are the owner of a small shop, and you want to have a chatbot available 
to answer questions from your data source, this is for you.

## How-to Guide

### 1. Create an OpenAI API token

If you haven't created any OpenAI account yet, please follow this [tutorial](https://fptshop.com.vn/tin-tuc/thu-thuat/cach-tu-tao-tai-khoan-chatgpt-tai-viet-nam-154372) to create one.

Note that, you must use an VPN, and select USA before creating your new account. You can install [this VPN](https://chrome.google.com/webstore/detail/free-vpn-for-chrome-vpn-p/majdfhpaihoncoakbjgbdhglocklcgno) on your browser as I did ;).

After registering your account, navigate to https://platform.openai.com/account/api-keys and click on `Create new secret key`.


When you have already created your key, update your `.env.example` file to replace my key.

### 2. Run the API


```shell
    uvicorn main:app --host 0.0.0.0 --port 30000
```

Open your browser and access this address `localhost:30000/docs` to access API doc (Swagger UI).

### 3. Enjoy your API

There are two routes in the Swagger UI:

- `/chatGPT`: Press `Try it out`, then enter `username`: `bbuser` and `password`: `1234` to authenticate.
After that, enter the text as the `/chat` route.