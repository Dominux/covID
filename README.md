# covID
#### VK bot for publishing a statistic in vk clubs




## Quick start
1. Clone this repo
2. Put:
    * Your image into `static/images/` 
    * Your font into `static/fonts/`
3. Change `data_config.json` according to this:
    * `"env"`: `"prod"` or `"dev"`
    * `"dev"`: your vk login, vk app info, and clubs info, time info. This data exists to be used for developing and testing
    * `"prod"`: similar to `"dev"`, but for production. Be carefully!!!
    * `"image"`: all data according to the image what you are going to use (I hope you will deal with it)
4. Run `app.py`

## Disadvantages (what is planned to change)
1. Close-to-code image processing. To set what you want you need do a lot of manipulations, such as:
    * Set right `xy` coordinates
    * Write it into `data_config.json` (thx at least for reloading data_config at an every publishing iteration)
    * Upload image and font files into those directories (yep, it's reloaded too, I've decided at least this problem already)
    * And... who knows, u can get an error, or a bad attachment due to invalid data :(

And anyway, it has to be rewrited on server itself! Wht's the f... It's so terrible and you know it

2. `@error_handler` logs errors into console - I think it should send me error if that appears

3. If you want to use another website to get info, you need rewrite `Action._parse_statistic_response` (I think it isn't a program disadvantage, moreover *it's something of a great architecture decision itself*)
![](delete_me_after_reading_readme/image.jpg)
