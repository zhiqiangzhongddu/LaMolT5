- Generate an API key and you can get free tokens if you do research on 
- Set up gemini API key in the environment variable `api_key` in `openai\prompts_single_rewrite_check.py`.
- Run the following command to generate the script:

  ```
  # Or python .\openai\prompts_single_rewrite_check.py -h for help
  python .\openai\prompts_single_rewrite_check.py
  # python openai/prompts_single_rewrite_check.py --p aoai -m gpt-35-turbo-0125
  ```
- The script will generate files in the `rewritings_openai` folder. The files will be named `{cid}.txt` where `cid` is the caption id.
- The script will also generate files `error_log.txt` and `error_cids.txt`,  in the `openai` folder, which will contain the error logs and the caption ids for which the script failed to generate rewrites.
- When running the script, you can see the progress bar in the terminal, sometimes the progress bar may seem stuck, because some of request may is timeout or server may overload, openai has a longest request time of 600 seconds, the script will move on to the next request and record the failed request in the error log.
- The script will also print the number of failed rewrites, if the the number of failed rewrites is small, you can leave it to us to handle the failed rewrites.
- If you close the terminal, you can just re-run it and our script will continue from where it left off.
