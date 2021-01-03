from bs4 import BeautifulSoup as bs
import configuration as cfg
import requests


class Web_scrap:

    @staticmethod
    def web_scrap(section, number, price, color=None):
        """
        :param section: the user's chosen product type (DRESSES, TOPS, SWIMWEAR)
        :param number: number of products to scrap
        :param price: max price of products
        :param color: color of products
        :return: url according to the user's choice, number of products and section
        This function use the html of the main page, get into the page of chosen product (DRESSES, TOPS,
        SWIMWEAR) and the user's choices: number of products, max price and color of product.
        This function create list of url for the product, and call the product_info() function in order to get the info
         for each product in the list.
        """

        # create html of main page
        soup = bs(requests.get(cfg.URL).content, cfg.HTML_PRS)

        # find the section URL
        products_url_page = str(soup.find(cfg.URL_PAGE_FIND_TYPE,
                                          {cfg.URL_PAGE_TITLE: section})
                                ).split(cfg.PRODUCT_URL_PAGE_SPLIT)[cfg.PRODUCT_URL_PAGE_SPLIT_NUM]

        # create html of products page (by the section)
        soup = bs(requests.get(products_url_page).content, cfg.HTML_PRS)

        if color is not None:
            # find all the url of the product by different colors
            prod_color = str(soup.find_all(cfg.PROD_COLOR_SPAN,
                                           {cfg.PROD_COLOR_CLASS: cfg.PROD_COLOR_CLASS_NAME})
                             ).split(cfg.PROD_COLOR_SPLIT_SIGN)
            all_url = []
            for y in [x.split() for x in prod_color if cfg.HREF in x]:
                all_url.append(cfg.URL + " ".join([x.split(cfg.HREF) for x in y if cfg.HREF in x]
                                                  [cfg.LOOP_COLOR_NUM]).strip().strip(cfg.STRIP_SIGN))

            # create dict of colors and the url by color
            color_dict = dict(zip(cfg.COLORS_LIST, all_url))

            # create the url by the price range
            url_choice = color_dict[color] + cfg.URL_CHOICE_PRICE.format(str(cfg.LOW_PRICE), str(price))

        else:
            url_choice = cfg.URL + products_url_page + cfg.URL_CHOICE_PRICE.format(str(cfg.LOW_PRICE), str(price))

        return url_choice, number, section
