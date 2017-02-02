# ft_converter

Extract transactions from Franklin Templeton (FT) files and convert them to Advent Geneva system's trade quick import format. The transactions include:

1. Buy/Sell trades.
2. Bond transfers.
3. Bond events: call, paydown, tender offer.
4. Cash transfers.



+++++++++++
How to use
+++++++++++

To extract transactions from a single file and write into csv output, use

	python ft_main.py <ft_file> --type <transaction_type>

	where <transaction_type> can be:
	1. fx: FX buy sell trades.


To run unit test, use

	nose2



+++++++++++
ver 0.1
+++++++++++
1. FX record conversion ready.
