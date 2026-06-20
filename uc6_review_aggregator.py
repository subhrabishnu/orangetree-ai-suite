"""
OrangeTree Global — Review & Sentiment Aggregator (UC6)
Multi-platform review analysis for F&B / SME clients
Powered by Claude API (Anthropic)
Run: streamlit run uc6_review_aggregator.py
"""

import streamlit as st
import anthropic
import json
from datetime import datetime

# -- Embedded logo (base64) so no separate SVG file needed on Streamlit Cloud --
LOGO_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjUgOSAxNTg2IDI2OCIgd2lkdGg9IjE1ODYiIGhlaWdodD0iMjY4Ij48dGl0bGU+T3JhbmdlVHJlZS57YWl9PC90aXRsZT48cGF0aCBmaWxsPSIjMUE3QTMwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xODIuNSAxM0wxODMuNSAxM0wxODMuNSAxOEwxODIuNSAxOUwxODIuNSAyMkwxODEuNSAyM0wxODAuNSAyOEwxNzguNSAzMUwxNzguNSAzM0wxNzMuNSA0M0wxNzEuNSA0NUwxNjcuNSA1MkwxNjMuNSA1NkwxNjMuNSA1N0wxNTMgNjcuNUwxNTIgNjcuNUwxNDUgNzMuNUwxNDIgNzQuNUwxNDAgNzYuNUwxMzYgNzguNUwxMzQgNzguNUwxMzAgODAuNUwxMjcgODAuNUwxMjYgODEuNUwxMTYgODEuNUwxMTUgODAuNUwxMTIgODAuNUwxMDUgNzYuNUwxMDAuNSA3MkwxMDAuNSA3MUwxMDYgNjguNUwxMDggNjYuNUwxMTUgNjIuNUwxMTggNTkuNUwxMTkgNTkuNUwxMjQgNTQuNUwxMjUgNTQuNUwxMzEuNSA0OEwxMzEuNSA0N0wxMzAgNDYuNUwxMTUgNTQuNUwxMTMgNTQuNUwxMDkgNTYuNUwxMDYgNTYuNUwxMDUgNTcuNUw5NiA1Ny41TDk1IDU2LjVMOTMgNTYuNUw4OC41IDUxTDg4LjUgNDRMOTIuNSAzNUw5NS41IDMyTDk1LjUgMzFMMTAzIDI0LjVMMTEyIDIwLjVMMTE5IDIwLjVMMTIwIDE5LjVMMTQ4IDE5LjVMMTQ5IDE4LjVMMTU5IDE4LjVMMTYwIDE3LjVMMTY2IDE3LjVMMTY3IDE2LjVMMTcxIDE2LjVMMTcyIDE1LjVMMTc1IDE1LjVMMTc2IDE0LjVMMTgyIDEzLjVaTTI5LjUgMTdMMzAgMTYuNUwzNCAyMC41TDM1IDIwLjVMNDAgMjQuNUw1MiAzMC41TDU0IDMwLjVMNjMgMzUuNUw2NSAzNS41TDY3IDM3LjVMNzIgMzkuNUw3NSA0Mi41TDc2IDQyLjVMODIuNSA1MEw4Mi41IDUyTDg0LjUgNTZMODQuNSA2MEw4MyA2MS41TDc3IDYyLjVMNzYgNjMuNUw2OCA2My41TDY3IDY0LjVMNjYgNjMuNUw1OSA2My41TDU4IDYyLjVMNTUgNjIuNUw0NiA1Ny41TDM4LjUgNDlMMzQuNSA0MUwzMy41IDM1TDMyLjUgMzRMMzIuNSAzMUwzMS41IDMwTDMxLjUgMjRMMzAuNSAyM0wzMCAxNy41Wk0xMzEuNSA0NkwxMzIgNDUuNUwxMzIgNDYuNVoiPjwvcGF0aD48cGF0aCBmaWxsPSIjRjM2NjIxIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik05My41IDg3TDExOSA4Ni41TDEyMCA4Ny41TDEyNCA4Ny41TDEyNSA4OC41TDEzMyA5MC41TDE0MyA5NS41TDE0NSA5Ny41TDE1MiAxMDEuNUwxNTYgMTA1LjVMMTU3IDEwNS41TDE2Ni41IDExNUwxNjYuNSAxMTZMMTcwLjUgMTIwTDE3MC41IDEyMUwxNzMuNSAxMjRMMTc0LjUgMTI3TDE3Ni41IDEyOUwxODEuNSAxMzlMMTgxLjUgMTQxTDE4Mi41IDE0MkwxODIuNSAxNDRMMTg1LjUgMTUxTDE4NS41IDE1NEwxODYuNSAxNTVMMTg2LjUgMTYwTDE4Ny41IDE2MUwxODcuNSAxODFMMTg2LjUgMTgyTDE4Ni41IDE4OEwxODUuNSAxODlMMTg1LjUgMTkzTDE4My41IDE5N0wxODIuNSAyMDNMMTc5LjUgMjA4TDE3OS41IDIxMEwxNzcuNSAyMTRMMTc1LjUgMjE2TDE3NC41IDIxOUwxNjcuNSAyMjhMMTY3LjUgMjI5TDE1NSAyNDEuNUwxNTQgMjQxLjVMMTUxIDI0NC41TDE1MCAyNDQuNUwxNDUgMjQ4LjVMMTQyIDI0OS41TDE0MCAyNTEuNUwxMzYgMjUzLjVMMTM0IDI1My41TDEyOSAyNTYuNUwxMjMgMjU3LjVMMTE5IDI1OS41TDExNSAyNTkuNUwxMTQgMjYwLjVMMTA4IDI2MC41TDEwNyAyNjEuNUw4OSAyNjEuNUw4OCAyNjAuNUw4MiAyNjAuNUw4MSAyNTkuNUw3MyAyNTguNUw3MiAyNTcuNUw2NyAyNTYuNUw2NCAyNTQuNUw2MiAyNTQuNUw1MiAyNDkuNUw0MyAyNDIuNUw0MiAyNDIuNUwyNi41IDIyN0wyNi41IDIyNkwyMC41IDIxOEwxMi41IDIwMUwxMS41IDE5NUwxMC41IDE5NEwxMC41IDE5MUw5LjUgMTkwTDkuNSAxODVMOC41IDE4NEw4LjUgMTYyTDkuNSAxNjFMMTAuNSAxNTNMMTEuNSAxNTJMMTMuNSAxNDRMMTYuNSAxMzhMMTguNSAxMzZMMjEuNSAxMzBMMzEgMTE5LjVMMzEuNSAxMjBMMjQuNSAxMzNMMjQuNSAxMzVMMjEuNSAxNDJMMjEuNSAxNTVMMjQuNSAxNjFMMzAgMTY1LjVMMzYgMTY4LjVMNDQgMTY5LjVMNDUgMTcwLjVMNzEgMTcwLjVMNzIgMTY5LjVMNzYgMTY5LjVMNzcgMTY4LjVMODAgMTY4LjVMODEgMTY3LjVMODkgMTY1LjVMMTA1IDE1Ny41TDEwNyAxNTUuNUwxMTQgMTUxLjVMMTMxLjUgMTM1TDEzMS41IDEzNEwxMzYuNSAxMjhMMTQwLjUgMTE5TDE0MC41IDEwOUwxMzguNSAxMDVMMTMyIDk4LjVMMTI0IDk0LjVMMTIwIDk0LjVMMTE5IDkzLjVMMTA0IDkzLjVMMTAzIDk0LjVMOTUgOTUuNUw5NCA5Ni41TDg5IDk3LjVMODQgMTAwLjVMODIgMTAwLjVMODAgMTAyLjVMNzcgMTAzLjVMNzEgMTA4LjVMNzAgMTA4LjVMNjAuNSAxMThMNjAuNSAxMTlMNTcuNSAxMjJMNTYuNSAxMjVMNTQuNSAxMjdMNTQuNSAxMjlMNTIuNSAxMzNMNTIuNSAxNDFMNTQuNSAxNDVMNTcgMTQ3LjVMNjMgMTUwLjVMNzQgMTUwLjVMNzUgMTQ5LjVMNzkgMTQ4LjVMODQuNSAxNDNMODUuNSAxNDFMODUuNSAxMzNMODQuNSAxMzJMODMuNSAxMjdMNzcuNSAxMTlMODUgMTE0LjVMODcgMTE0LjVMOTMgMTExLjVMOTYgMTExLjVMOTcgMTEwLjVMMTExIDExMC41TDExNy41IDExNkwxMTcuNSAxMThMMTE4LjUgMTE5TDExOC41IDEyNEwxMTcuNSAxMjVMMTE3LjUgMTI4TDExMi41IDEzN0wxMDMgMTQ2LjVMOTAgMTU0LjVMODggMTU0LjVMODUgMTU2LjVMODMgMTU2LjVMNzkgMTU4LjVMNzYgMTU4LjVMNzUgMTU5LjVMNzAgMTU5LjVMNjkgMTYwLjVMNTMgMTYwLjVMNTIgMTU5LjVMNDggMTU5LjVMNDcgMTU4LjVMNDIgMTU3LjVMMzUgMTUzLjVMMzAuNSAxNDhMMzAuNSAxNDZMMjguNSAxNDJMMjguNSAxMzZMMjkuNSAxMzVMMjkuNSAxMzFMMzQuNSAxMjFMMzcuNSAxMThMMzcuNSAxMTdMNDcgMTA3LjVMNDggMTA3LjVMNTIgMTAzLjVMNTMgMTAzLjVMNTggOTkuNUw3MiA5Mi41TDc0IDkyLjVMNzUgOTEuNUw3NyA5MS41TDg0IDg4LjVMODcgODguNUw4OCA4Ny41TDkzIDg3LjVaIj48L3BhdGg+PHBhdGggZmlsbD0iIzAwMDAwMCIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMjcwLjUgNzFMMjc3IDcwLjVMMjc4IDcxLjVMMjg3IDcxLjVMMjg4IDcyLjVMMjkyIDcyLjVMMjk2IDc0LjVMMjk5IDc0LjVMMzAyIDc2LjVMMzA0IDc2LjVMMzEwIDc5LjVMMzE5IDg2LjVMMzIwIDg2LjVMMzI4LjUgOTVMMzI4LjUgOTZMMzMzLjUgMTAyTDMzNC41IDEwNUwzMzYuNSAxMDdMMzM5LjUgMTEzTDMzOS41IDExNUwzNDEuNSAxMThMMzQyLjUgMTI0TDM0NC41IDEyOEwzNDUuNSAxMzhMMzQ2LjUgMTM5TDM0Ni41IDE2OEwzNDUuNSAxNjlMMzQ0LjUgMTc5TDM0My41IDE4MEwzNDMuNSAxODNMMzQyLjUgMTg0TDM0MC41IDE5MkwzMzguNSAxOTVMMzM4LjUgMTk3TDMzNi41IDIwMUwzMzQuNSAyMDNMMzMzLjUgMjA2TDMyOC41IDIxMkwzMjguNSAyMTNMMzE1IDIyNS41TDMxNCAyMjUuNUwzMDkgMjI5LjVMMzAzIDIzMi41TDMwMSAyMzIuNUwyOTggMjM0LjVMMjkyIDIzNS41TDI5MSAyMzYuNUwyODggMjM2LjVMMjg3IDIzNy41TDI4MSAyMzcuNUwyODAgMjM4LjVMMjYzIDIzOC41TDI2MiAyMzcuNUwyNTcgMjM3LjVMMjU2IDIzNi41TDI0OSAyMzUuNUwyNDEgMjMxLjVMMjM5IDIzMS41TDIzNyAyMjkuNUwyMzQgMjI4LjVMMjMyIDIyNi41TDIyOCAyMjQuNUwyMTMuNSAyMDlMMjEwLjUgMjAzTDIwOC41IDIwMUwyMDcuNSAxOTdMMjA0LjUgMTkyTDIwNC41IDE5MEwyMDIuNSAxODZMMjAyLjUgMTgzTDIwMS41IDE4MkwyMDEuNSAxNzlMMjAwLjUgMTc4TDIwMC41IDE3M0wxOTkuNSAxNzJMMTk4LjUgMTUwTDE5OS41IDE0OUwxOTkuNSAxNDBMMjAwLjUgMTM5TDIwMC41IDEzNEwyMDEuNSAxMzNMMjAyLjUgMTI2TDIwMy41IDEyNUwyMDQuNSAxMjBMMjA2LjUgMTE3TDIwNi41IDExNUwyMTAuNSAxMDdMMjEyLjUgMTA1TDIxNi41IDk4TDIyOSA4NS41TDIzMCA4NS41TDIzOCA3OS41TDI0MiA3Ny41TDI0NCA3Ny41TDI0NyA3NS41TDI1MiA3NC41TDI1MyA3My41TDI2MSA3Mi41TDI2MiA3MS41TDI3MCA3MS41Wk0xMjgyLjUgNzFMMTI5MC41IDcxTDEyOTAuNSA4NEwxMjgwIDg0LjVMMTI3OSA4NS41TDEyNzcgODUuNUwxMjcwLjUgOTFMMTI2OC41IDk1TDEyNjguNSA5N0wxMjY3LjUgOThMMTI2Ny41IDExNEwxMjY4LjUgMTE1TDEyNjguNSAxMjFMMTI2OS41IDEyMkwxMjY5LjUgMTI4TDEyNzAuNSAxMjlMMTI3MC41IDE0OUwxMjY5LjUgMTUwTDEyNjguNSAxNTVMMTI2Ni41IDE1N0wxMjY2LjUgMTU4TDEyNjEgMTYzLjVMMTI1NyAxNjUuNUwxMjU1IDE2NS41TDEyNTQuNSAxNjdMMTI2MSAxNjkuNUwxMjY2LjUgMTc1TDEyNjkuNSAxODFMMTI2OS41IDE4NEwxMjcwLjUgMTg1TDEyNzAuNSAyMDVMMTI2OS41IDIwNkwxMjY4LjUgMjE5TDEyNjcuNSAyMjBMMTI2Ny41IDIzNUwxMjY4LjUgMjM2TDEyNjguNSAyMzlMMTI3MC41IDI0M0wxMjc0IDI0Ni41TDEyODEgMjQ5LjVMMTI5MC41IDI1MEwxMjkwLjUgMjYyTDEyNzYgMjYyLjVMMTI3NSAyNjEuNUwxMjY5IDI2MC41TDEyNjMgMjU3LjVMMTI1NS41IDI1MEwxMjUyLjUgMjQ0TDEyNTIuNSAyNDJMMTI1MS41IDI0MUwxMjUxLjUgMjM2TDEyNTAuNSAyMzVMMTI1MS41IDIxNUwxMjUyLjUgMjE0TDEyNTIuNSAyMDhMMTI1My41IDIwN0wxMjUzLjUgMjAxTDEyNTQuNSAyMDBMMTI1NC41IDE4NUwxMjUzLjUgMTg0TDEyNTIuNSAxODBMMTI0OCAxNzUuNUwxMjQ0IDE3NC41TDEyNDMgMTczLjVMMTIzOSAxNzMuNUwxMjM1LjUgMTcyTDEyMzUuNSAxNjFMMTI0NCAxNTkuNUwxMjUwIDE1Ni41TDEyNTEuNSAxNTVMMTI1NC41IDE0OEwxMjU0LjUgMTMzTDEyNTMuNSAxMzJMMTI1My41IDEyNUwxMjUyLjUgMTI0TDEyNTEuNSAxMTBMMTI1MC41IDEwOUwxMjUwLjUgOThMMTI1MS41IDk3TDEyNTIuNSA4OUwxMjU2LjUgODJMMTI2NCA3NS41TDEyNzEgNzIuNUwxMjc0IDcyLjVMMTI3NSA3MS41TDEyODIgNzEuNVpNMTQyMC41IDcxTDE0MjggNzAuNUwxNDI5IDcxLjVMMTQzNiA3MS41TDE0MzcgNzIuNUwxNDQzIDczLjVMMTQ1MCA3Ny41TDE0NTUuNSA4M0wxNDU4LjUgODlMMTQ1OS41IDk1TDE0NjAuNSA5NkwxNDYwLjUgMTEyTDE0NTkuNSAxMTNMMTQ1OS41IDEyMEwxNDU4LjUgMTIxTDE0NTcuNSAxMzZMMTQ1Ni41IDEzN0wxNDU2LjUgMTQ2TDE0NTcuNSAxNDdMMTQ1Ny41IDE1MUwxNDYzIDE1Ny41TDE0NjcgMTU5LjVMMTQ3Ni41IDE2MUwxNDc2LjUgMTcyTDE0NzMgMTcyLjVMMTQ3MiAxNzMuNUwxNDY4IDE3My41TDE0NjIgMTc2LjVMMTQ1OC41IDE4MUwxNDU3LjUgMTgzTDE0NTcuNSAxODZMMTQ1Ni41IDE4N0wxNDU3LjUgMjA1TDE0NTguNSAyMDZMMTQ1OS41IDIyMEwxNDYwLjUgMjIxTDE0NjAuNSAyMzdMMTQ1OS41IDIzOEwxNDU5LjUgMjQyTDE0NTYuNSAyNDlMMTQ1MSAyNTUuNUwxNDUwIDI1NS41TDE0NDUgMjU5LjVMMTQ0MyAyNTkuNUwxNDM5IDI2MS41TDE0MzYgMjYxLjVMMTQzNSAyNjIuNUwxNDIwLjUgMjYyTDE0MjAuNSAyNTBMMTQzMCAyNDkuNUwxNDMxIDI0OC41TDE0MzMgMjQ4LjVMMTQzNyAyNDYuNUwxNDQwLjUgMjQzTDE0NDIuNSAyMzlMMTQ0Mi41IDIzN0wxNDQzLjUgMjM2TDE0NDMuNSAyMThMMTQ0Mi41IDIxN0wxNDQyLjUgMjEwTDE0NDEuNSAyMDlMMTQ0MS41IDIwNEwxNDQwLjUgMjAzTDE0NDAuNSAxODZMMTQ0MS41IDE4NUwxNDQyLjUgMTc5TDE0NDUuNSAxNzRMMTQ1MiAxNjguNUwxNDU2LjUgMTY3TDE0NTYgMTY1LjVMMTQ1MiAxNjQuNUwxNDQ1LjUgMTU5TDE0NDIuNSAxNTRMMTQ0Mi41IDE1MkwxNDQwLjUgMTQ4TDE0NDAuNSAxMzFMMTQ0MS41IDEzMEwxNDQxLjUgMTI0TDE0NDIuNSAxMjNMMTQ0Mi41IDExN0wxNDQzLjUgMTE2TDE0NDMuNSA5N0wxNDQyLjUgOTZMMTQ0Mi41IDk0TDE0NDEuNSA5MkwxNDM2IDg2LjVMMTQzNCA4NS41TDE0MzIgODUuNUwxNDMxIDg0LjVMMTQyMSA4NC41TDE0MjAuNSA3MlpNMTU4NC41IDczTDE1ODcuNSA3M0wxNTg3IDkxLjVMMTU4Ni41IDgzTDE1ODUuNSA4MkwxNTg1LjUgNzZMMTU4NC41IDc0Wk04MjkuNSA3NEw5NDkuNSA3NEw5NDkgOTEuNUw5MDAuNSA5Mkw5MDAgMjM1LjVMODc5LjUgMjM1TDg3OS41IDkyTDgzMCA5MS41TDgyOS41IDc1Wk0xNDAwLjUgNzRMMTQwOCA3My41TDE0MDkgNzQuNUwxNDExIDc0LjVMMTQxNi41IDgwTDE0MTYuNSA4MkwxNDE3LjUgODNMMTQxNy41IDkxTDE0MTYuNSA5M0wxNDExIDk4LjVMMTQwOSA5OC41TDE0MDggOTkuNUwxNDAxIDk5LjVMMTQwMCA5OC41TDEzOTggOTguNUwxMzkyLjUgOTNMMTM5Mi41IDkxTDEzOTEuNSA5MEwxMzkxLjUgODNMMTM5Mi41IDgyTDEzOTIuNSA4MEwxMzk4IDc0LjVMMTQwMCA3NC41Wk0yNjMuNSA4OUwyODIgODguNUwyODMgODkuNUwyODYgODkuNUwyODcgOTAuNUwyODkgOTAuNUwyOTYgOTMuNUwzMDIgOTguNUwzMDMgOTguNUwzMDguNSAxMDRMMzA4LjUgMTA1TDMxNS41IDExNEwzMTguNSAxMjBMMzE4LjUgMTIyTDMxOS41IDEyM0wzMTkuNSAxMjVMMzIyLjUgMTMyTDMyMy41IDE0MkwzMjQuNSAxNDNMMzI0LjUgMTY2TDMyMy41IDE2N0wzMjMuNSAxNzJMMzIyLjUgMTczTDMyMi41IDE3N0wzMjEuNSAxNzhMMzIwLjUgMTg0TDMxOC41IDE4N0wzMTguNSAxODlMMzE0LjUgMTk3TDMxMi41IDE5OUwzMTAuNSAyMDNMMzAxIDIxMi41TDI5MyAyMTcuNUwyOTEgMjE3LjVMMjg4IDIxOS41TDI4NSAyMTkuNUwyODQgMjIwLjVMMjgwIDIyMC41TDI3OSAyMjEuNUwyNjcgMjIxLjVMMjY2IDIyMC41TDI2MiAyMjAuNUwyNjEgMjE5LjVMMjU4IDIxOS41TDI1NSAyMTcuNUwyNTMgMjE3LjVMMjQ1IDIxMi41TDIzNS41IDIwM0wyMjYuNSAxODdMMjI2LjUgMTg1TDIyNC41IDE4MUwyMjQuNSAxNzhMMjIzLjUgMTc3TDIyMy41IDE3NEwyMjIuNSAxNzNMMjIyLjUgMTY4TDIyMS41IDE2N0wyMjEuNSAxNDRMMjIyLjUgMTQzTDIyMi41IDEzN0wyMjMuNSAxMzZMMjIzLjUgMTMzTDIyNC41IDEzMkwyMjQuNSAxMjlMMjI1LjUgMTI4TDIyNy41IDEyMEwyMzMuNSAxMDlMMjQ0IDk3LjVMMjU0IDkxLjVMMjU2IDkxLjVMMjYwIDg5LjVMMjYzIDg5LjVaTTQwMi41IDExN0w0MTAgMTE2LjVMNDEyLjUgMTE4TDQxMi41IDEzN0w0MTEgMTM3LjVMNDEwIDEzNi41TDQwMiAxMzYuNUw0MDEgMTM3LjVMMzk4IDEzNy41TDM5MSAxNDAuNUwzODEuNSAxNTFMMzc5LjUgMTU1TDM3OC41IDE2MEwzNzcuNSAxNjFMMzc3LjUgMTY0TDM3Ni41IDE2NUwzNzYuNSAyMzVMMzU1LjUgMjM1TDM1NS41IDEzNUwzNTQuNSAxMzRMMzU0LjUgMTIwTDM3Mi41IDEyMEwzNzIuNSAxMjVMMzczLjUgMTI2TDM3NCAxNDIuNUwzODAuNSAxMzBMMzg4IDEyMi41TDM5NSAxMTguNUwzOTcgMTE4LjVMMzk4IDExNy41TDQwMiAxMTcuNVpNNDQ2LjUgMTE3TDQ2MCAxMTYuNUw0NjEgMTE3LjVMNDY2IDExNy41TDQ2NyAxMTguNUw0NzMgMTE5LjVMNDc5IDEyMi41TDQ4OC41IDEzMUw0OTQuNSAxNDJMNDk1LjUgMTQ4TDQ5Ni41IDE0OUw0OTYuNSAxNTRMNDk3LjUgMTU1TDQ5Ny41IDIyM0w0OTguNSAyMjRMNDk4LjUgMjMzTDQ5OS41IDIzNUw0ODEgMjM1LjVMNDc5LjUgMjM0TDQ3OS41IDIyNkw0NzguNSAyMjVMNDc4IDIyMS41TDQ2OSAyMzAuNUw0NjAgMjM1LjVMNDU4IDIzNS41TDQ1NCAyMzcuNUw0NTAgMjM3LjVMNDQ5IDIzOC41TDQzNiAyMzguNUw0MzUgMjM3LjVMNDMxIDIzNy41TDQzMCAyMzYuNUw0MjggMjM2LjVMNDE5IDIzMS41TDQxMy41IDIyNkw0MDguNSAyMTdMNDA3LjUgMjExTDQwNi41IDIxMEw0MDYuNSAyMDBMNDA3LjUgMTk5TDQwNy41IDE5NUw0MDguNSAxOTRMNDEwLjUgMTg3TDQxMi41IDE4NUw0MTQuNSAxODFMNDE5IDE3Ni41TDQyMCAxNzYuNUw0MjYgMTcxLjVMNDMyIDE2OC41TDQzNCAxNjguNUw0MzcgMTY2LjVMNDQwIDE2Ni41TDQ0NCAxNjQuNUw0NTQgMTYzLjVMNDU1IDE2Mi41TDQ2NCAxNjIuNUw0NjUgMTYxLjVMNDc2LjUgMTYxTDQ3Ni41IDE1Mkw0NzUuNSAxNTFMNDc1LjUgMTQ4TDQ3Mi41IDE0Mkw0NjcgMTM2LjVMNDYxIDEzMy41TDQ1OCAxMzMuNUw0NTcgMTMyLjVMNDQyIDEzMi41TDQ0MSAxMzMuNUw0MzcgMTMzLjVMNDM2IDEzNC41TDQyOCAxMzYuNUw0MjEgMTQwLjVMNDE5LjUgMTQwTDQxNy41IDEzM0w0MTYuNSAxMzJMNDE2LjUgMTMwTDQxNS41IDEyOUw0MTUuNSAxMjdMNDE3IDEyNS41TDQzMSAxMTkuNUw0MzQgMTE5LjVMNDM1IDExOC41TDQzOCAxMTguNUw0MzkgMTE3LjVMNDQ2IDExNy41Wk01NjUuNSAxMTdMNTc2IDExNi41TDU3NyAxMTcuNUw1ODIgMTE3LjVMNTg4IDEyMC41TDU5MCAxMjAuNUw1OTIgMTIyLjVMNTk1IDEyMy41TDYwMy41IDEzMkw2MDkuNSAxNDNMNjA5LjUgMTQ2TDYxMS41IDE1MEw2MTEuNSAxNTVMNjEyLjUgMTU2TDYxMi41IDIzNUw1OTEuNSAyMzVMNTkxLjUgMTYyTDU5MC41IDE2MUw1OTAuNSAxNTZMNTg5LjUgMTU1TDU4OS41IDE1Mkw1ODUuNSAxNDRMNTc3IDEzNi41TDU3NSAxMzYuNUw1NzEgMTM0LjVMNTU5IDEzNC41TDU1OCAxMzUuNUw1NTUgMTM1LjVMNTQ5IDEzOC41TDUzOS41IDE0OEw1MzYuNSAxNTRMNTM2LjUgMTU2TDUzNS41IDE1N0w1MzUuNSAxNjJMNTM0LjUgMTYzTDUzNC41IDIzNUw1MTMuNSAyMzVMNTEzLjUgMTI1TDUxMi41IDEyNEw1MTIuNSAxMjBMNTMxIDExOS41TDUzMyAxMzguNUw1MzUuNSAxMzRMNTQ1IDEyNC41TDU0NiAxMjQuNUw1NDggMTIyLjVMNTU3IDExOC41TDU2NSAxMTcuNVpNNjY3LjUgMTE3TDY3OCAxMTYuNUw2NzkgMTE3LjVMNjg0IDExNy41TDY4NSAxMTguNUw2ODggMTE4LjVMNjk4IDEyMy41TDcwNi41IDEzMkw3MDkgMTM2LjVMNzA5LjUgMTMwTDcxMC41IDEyOUw3MTEgMTE5LjVMNzI5LjUgMTIwTDcyOS41IDEyM0w3MjguNSAxMjRMNzI4LjUgMjI4TDcyNy41IDIyOUw3MjcuNSAyMzlMNzI2LjUgMjQwTDcyNS41IDI0OUw3MjQuNSAyNTBMNzIzLjUgMjU1TDcxNy41IDI2Nkw3MDggMjc1LjVMNzA2IDI3Ni41TDYzMC41IDI3Nkw2MzEuNSAyNzVMNjMxLjUgMjczTDYzMi41IDI3Mkw2MzIuNSAyNzBMNjMzLjUgMjY5TDYzMy41IDI2N0w2MzQuNSAyNjZMNjM2IDI2MC41TDY0MyAyNjQuNUw2NDUgMjY0LjVMNjUyIDI2Ny41TDY1NSAyNjcuNUw2NTYgMjY4LjVMNjYxIDI2OC41TDY2MiAyNjkuNUw2NzcgMjY5LjVMNjc4IDI2OC41TDY4MiAyNjguNUw2ODMgMjY3LjVMNjg4IDI2Ni41TDY5OC41IDI1OUw3MDQuNSAyNDlMNzA1LjUgMjQzTDcwNi41IDI0Mkw3MDYuNSAyMzhMNzA3LjUgMjM3TDcwNyAyMTYuNUw3MDUuNSAyMTlMNjk3IDIyNy41TDY4OCAyMzIuNUw2ODIgMjMzLjVMNjgxIDIzNC41TDY3NyAyMzQuNUw2NzYgMjM1LjVMNjY1IDIzNS41TDY2NCAyMzQuNUw2NTkgMjM0LjVMNjQ1IDIyOC41TDY0MyAyMjYuNUw2NDIgMjI2LjVMNjMyLjUgMjE3TDYzMi41IDIxNkw2MjkuNSAyMTNMNjI0LjUgMjAzTDYyNC41IDIwMUw2MjIuNSAxOTdMNjIyLjUgMTk0TDYyMS41IDE5M0w2MjEuNSAxODhMNjIwLjUgMTg3TDYyMC41IDE2OUw2MjEuNSAxNjhMNjIxLjUgMTYzTDYyMi41IDE2Mkw2MjMuNSAxNTVMNjI5LjUgMTQyTDYzMS41IDE0MEw2MzMuNSAxMzZMNjQzIDEyNi41TDY0NCAxMjYuNUw2NDkgMTIyLjVMNjUzIDEyMC41TDY2MSAxMTguNUw2NjIgMTE3LjVMNjY3IDExNy41Wk03ODUuNSAxMTdMNzk3IDExNi41TDc5OCAxMTcuNUw4MDMgMTE3LjVMODA0IDExOC41TDgxMCAxMTkuNUw4MTkgMTI0LjVMODI4LjUgMTM0TDgzMy41IDE0Mkw4MzMuNSAxNDRMODM1LjUgMTQ3TDgzNS41IDE0OUw4MzcuNSAxNTNMODM4LjUgMTYzTDgzOS41IDE2NEw4MzkuNSAxNzhMODM4IDE4MS41TDc1OCAxODEuNUw3NTcuNSAxOTBMNzU4LjUgMTkxTDc1OC41IDE5NUw3NTkuNSAxOTZMNzU5LjUgMTk4TDc2NS41IDIwOUw3NzAgMjEzLjVMNzcxIDIxMy41TDc3NiAyMTcuNUw3ODMgMjE5LjVMNzg0IDIyMC41TDc4NyAyMjAuNUw3ODggMjIxLjVMODEwIDIyMS41TDgxMSAyMjAuNUw4MTYgMjIwLjVMODE3IDIxOS41TDgyMCAyMTkuNUw4MjEgMjE4LjVMODI2IDIxNy41TDgyOSAyMTUuNUw4MjkuNSAyMTlMODMwLjUgMjIwTDgzMC41IDIyM0w4MzEuNSAyMjRMODMxLjUgMjI3TDgzMi41IDIyOEw4MzIuNSAyMzFMODMwIDIzMi41TDgyMiAyMzQuNUw4MjEgMjM1LjVMODE3IDIzNS41TDgxNiAyMzYuNUw4MTIgMjM2LjVMODExIDIzNy41TDgwMiAyMzcuNUw4MDEgMjM4LjVMNzg4IDIzOC41TDc4NyAyMzcuNUw3ODEgMjM3LjVMNzgwIDIzNi41TDc3NyAyMzYuNUw3NzYgMjM1LjVMNzcwIDIzNC41TDc1OSAyMjguNUw3NTAuNSAyMjFMNzUwLjUgMjIwTDc0Ni41IDIxNkw3NDUuNSAyMTNMNzQyLjUgMjA5TDc0Mi41IDIwN0w3NDAuNSAyMDRMNzQwLjUgMjAyTDczOC41IDE5OEw3MzguNSAxOTRMNzM3LjUgMTkzTDczNy41IDE4Nkw3MzYuNSAxODVMNzM2LjUgMTc0TDczNy41IDE3M0w3MzcuNSAxNjZMNzM4LjUgMTY1TDczOC41IDE2MUw3MzkuNSAxNjBMNzM5LjUgMTU3TDc0MC41IDE1Nkw3NDEuNSAxNTFMNzQ4LjUgMTM4TDc1My41IDEzM0w3NTMuNSAxMzJMNzYxIDEyNS41TDc3MCAxMjAuNUw3NzIgMTIwLjVMNzc5IDExNy41TDc4NSAxMTcuNVpNOTk1LjUgMTE3TDEwMDQgMTE2LjVMMTAwNi41IDExOEwxMDA2LjUgMTM3TDEwMDUgMTM3LjVMMTAwNCAxMzYuNUw5OTYgMTM2LjVMOTk1IDEzNy41TDk5MSAxMzcuNUw5ODUgMTQwLjVMOTc5LjUgMTQ1TDk3OS41IDE0Nkw5NzYuNSAxNDlMOTczLjUgMTU0TDk3My41IDE1Nkw5NzEuNSAxNjBMOTcxLjUgMTYzTDk3MC41IDE2NEw5NzAuNSAxNzBMOTY5LjUgMTcxTDk2OS41IDIzNUw5NDguNSAyMzVMOTQ4LjUgMTIwTDk2Ni41IDEyMEw5NjYuNSAxMzNMOTY3LjUgMTM0TDk2OCAxNDIuNUw5NjguNSAxNDBMOTczLjUgMTMxTDk4MiAxMjIuNUw5ODkgMTE4LjVMOTk1IDExNy41Wk0xMDQ5LjUgMTE3TDEwNjIgMTE2LjVMMTA2MyAxMTcuNUwxMDY4IDExNy41TDEwNjkgMTE4LjVMMTA3NCAxMTkuNUwxMDgyIDEyMy41TDEwODUgMTI2LjVMMTA4NiAxMjYuNUwxMDkzLjUgMTM1TDEwOTkuNSAxNDZMMTA5OS41IDE0OEwxMTAxLjUgMTUyTDExMDEuNSAxNTVMMTEwMi41IDE1NkwxMTAyLjUgMTYwTDExMDMuNSAxNjFMMTEwNCAxNjkuNUwxMTA2LjUgMTU2TDExMTEuNSAxNDRMMTExMy41IDE0MkwxMTE0LjUgMTM5TDExMTcuNSAxMzZMMTExNy41IDEzNUwxMTI5IDEyNC41TDExMzkgMTE5LjVMMTE0NSAxMTguNUwxMTQ2IDExNy41TDExNTEgMTE3LjVMMTE1MiAxMTYuNUwxMTY0IDExNi41TDExNjUgMTE3LjVMMTE3MCAxMTcuNUwxMTcxIDExOC41TDExNzQgMTE4LjVMMTE3NyAxMjAuNUwxMTgxIDEyMS41TDExODMgMTIzLjVMMTE4NyAxMjUuNUwxMTk0LjUgMTMzTDExOTQuNSAxMzRMMTE5OC41IDEzOUwxMjAxLjUgMTQ1TDEyMDEuNSAxNDdMMTIwNC41IDE1NEwxMjA0LjUgMTU4TDEyMDUuNSAxNTlMMTIwNS41IDE2N0wxMjA2LjUgMTY4TDEyMDYuNSAxNzVMMTIwNS41IDE3NkwxMjA1IDE4MS41TDExMjQgMTgxLjVMMTEyMy41IDE4NkwxMTI0LjUgMTg3TDExMjQuNSAxOTJMMTEyNS41IDE5M0wxMTI1LjUgMTk2TDExMjkuNSAyMDVMMTEzMS41IDIwN0wxMTMxLjUgMjA4TDExNDEgMjE2LjVMMTE0NyAyMTkuNUwxMTQ5IDIxOS41TDExNTAgMjIwLjVMMTE1NCAyMjAuNUwxMTU1IDIyMS41TDExNzcgMjIxLjVMMTE3OCAyMjAuNUwxMTgyIDIyMC41TDExODMgMjE5LjVMMTE5MCAyMTguNUwxMTkzIDIxNi41TDExOTYgMjE2LjVMMTE5OS41IDIzMUwxMTkxIDIzNC41TDExODggMjM0LjVMMTE4NyAyMzUuNUwxMTg0IDIzNS41TDExODMgMjM2LjVMMTE3OSAyMzYuNUwxMTc4IDIzNy41TDExNjkgMjM3LjVMMTE2OCAyMzguNUwxMTU1IDIzOC41TDExNTQgMjM3LjVMMTE0MyAyMzYuNUwxMTQyIDIzNS41TDExMzcgMjM0LjVMMTEyNyAyMjkuNUwxMTE1LjUgMjE5TDExMTUuNSAyMThMMTExMS41IDIxM0wxMTA1LjUgMTk5TDExMDUuNSAxOTVMMTEwNC41IDE5NEwxMTA0LjUgMTg5TDExMDMuNSAxODhMMTEwMyAxODEuNUwxMDIxLjUgMTgyTDEwMjEuNSAxODlMMTAyMi41IDE5MEwxMDIyLjUgMTk0TDEwMjMuNSAxOTVMMTAyNC41IDIwMEwxMDI4LjUgMjA3TDEwMzcgMjE1LjVMMTA0NSAyMTkuNUwxMDUxIDIyMC41TDEwNTIgMjIxLjVMMTA3NCAyMjEuNUwxMDc1IDIyMC41TDEwODAgMjIwLjVMMTA4MSAyMTkuNUwxMDg0IDIxOS41TDEwODUgMjE4LjVMMTA5MyAyMTYuNUwxMDk0LjUgMjE5TDEwOTQuNSAyMjJMMTA5NS41IDIyM0wxMDk1LjUgMjI2TDEwOTYuNSAyMjdMMTA5NiAyMzEuNUwxMDg5IDIzNC41TDEwODYgMjM0LjVMMTA4NSAyMzUuNUwxMDgyIDIzNS41TDEwODEgMjM2LjVMMTA3NiAyMzYuNUwxMDc1IDIzNy41TDEwNjcgMjM3LjVMMTA2NiAyMzguNUwxMDUzIDIzOC41TDEwNTIgMjM3LjVMMTA0NSAyMzcuNUwxMDQ0IDIzNi41TDEwNDEgMjM2LjVMMTA0MCAyMzUuNUwxMDMyIDIzMy41TDEwMjIgMjI3LjVMMTAxMi41IDIxOEwxMDEyLjUgMjE3TDEwMDguNSAyMTJMMTAwMy41IDIwMEwxMDAyLjUgMTkyTDEwMDEuNSAxOTFMMTAwMS41IDE2N0wxMDAyLjUgMTY2TDEwMDIuNSAxNjJMMTAwMy41IDE2MUwxMDAzLjUgMTU4TDEwMDQuNSAxNTdMMTAwNS41IDE1MkwxMDExLjUgMTQwTDEwMjQgMTI2LjVMMTAzNCAxMjAuNUwxMDM2IDEyMC41TDEwNDAgMTE4LjVMMTA0MyAxMTguNUwxMDQ0IDExNy41TDEwNDkgMTE3LjVaTTEzMjYuNSAxMTdMMTM0MCAxMTYuNUwxMzQxIDExNy41TDEzNDYgMTE3LjVMMTM0NyAxMTguNUwxMzUwIDExOC41TDEzNTEgMTE5LjVMMTM1NiAxMjAuNUwxMzY2LjUgMTI4TDEzNjYuNSAxMjlMMTM3MC41IDEzM0wxMzc0LjUgMTQxTDEzNzUuNSAxNDdMMTM3Ni41IDE0OEwxMzc2LjUgMTUyTDEzNzcuNSAxNTNMMTM3Ny41IDIxNEwxMzc4LjUgMjE1TDEzNzguNSAyMzBMMTM3OS41IDIzMUwxMzc5LjUgMjM1TDEzNjEgMjM1LjVMMTM2MC41IDIzMUwxMzU5LjUgMjMwTDEzNTkuNSAyMjJMMTM1OCAyMjEuNUwxMzU2LjUgMjI0TDEzNDggMjMxLjVMMTM0MCAyMzUuNUwxMzM4IDIzNS41TDEzMzQgMjM3LjVMMTMzMCAyMzcuNUwxMzI5IDIzOC41TDEzMTYgMjM4LjVMMTMxNSAyMzcuNUwxMzEyIDIzNy41TDEzMTEgMjM2LjVMMTMwNiAyMzUuNUwxMzAxIDIzMi41TDEyOTUuNSAyMjhMMTI5NS41IDIyN0wxMjkyLjUgMjI0TDEyODkuNSAyMTlMMTI4OS41IDIxN0wxMjg3LjUgMjEzTDEyODcuNSAxOTdMMTI4OC41IDE5NkwxMjg4LjUgMTkzTDEyOTMuNSAxODNMMTMwMiAxNzQuNUwxMzE1IDE2Ny41TDEzMTcgMTY3LjVMMTMyMSAxNjUuNUwxMzI0IDE2NS41TDEzMjUgMTY0LjVMMTMyOCAxNjQuNUwxMzI5IDE2My41TDEzNTYuNSAxNjFMMTM1Ni41IDE1MUwxMzU1LjUgMTUwTDEzNTUuNSAxNDdMMTM1MC41IDEzOUwxMzQ0IDEzNC41TDEzNDIgMTM0LjVMMTMzOCAxMzIuNUwxMzIyIDEzMi41TDEzMjEgMTMzLjVMMTMxNyAxMzMuNUwxMzE2IDEzNC41TDEzMDggMTM2LjVMMTMwNCAxMzguNUwxMzAyIDE0MC41TDEyOTkuNSAxNDBMMTI5OS41IDEzOEwxMjk4LjUgMTM3TDEyOTguNSAxMzVMMTI5NS41IDEyOEwxMjk2IDEyNi41TDEzMDMgMTIyLjVMMTMwNSAxMjIuNUwxMzExIDExOS41TDEzMTkgMTE4LjVMMTMyMCAxMTcuNUwxMzI2IDExNy41Wk0xMzkzLjUgMTIwTDE0MTUuNSAxMjBMMTQxNSAyMzUuNUwxMzkzLjUgMjM1TDEzOTMuNSAxMjFaTTc4Ni41IDEzMkw3OTMgMTMxLjVMNzk0IDEzMi41TDc5OCAxMzIuNUw4MDggMTM3LjVMODExLjUgMTQxTDgxNi41IDE1MEw4MTYuNSAxNTJMODE4LjUgMTU2TDgxOC41IDE2NEw4MTkuNSAxNjVMODE4IDE2Ni41TDc1OCAxNjYuNUw3NTcuNSAxNjNMNzU4LjUgMTYyTDc1OC41IDE1OUw3NTkuNSAxNThMNzYwLjUgMTUzTDc2NS41IDE0NEw3NzMgMTM2LjVMNzgyIDEzMi41TDc4NiAxMzIuNVpNMTA1MC41IDEzMkwxMDU3IDEzMS41TDEwNTggMTMyLjVMMTA2MiAxMzIuNUwxMDYzIDEzMy41TDEwNjUgMTMzLjVMMTA3MSAxMzYuNUwxMDc2LjUgMTQyTDEwODAuNSAxNDlMMTA4MC41IDE1MUwxMDgyLjUgMTU1TDEwODMuNSAxNjZMMTAyMiAxNjYuNUwxMDIxLjUgMTY0TDEwMjIuNSAxNjNMMTAyMi41IDE1OUwxMDIzLjUgMTU4TDEwMjMuNSAxNTZMMTAyNS41IDE1M0wxMDI2LjUgMTQ5TDEwMjguNSAxNDdMMTAzMC41IDE0M0wxMDM5IDEzNS41TDEwNDYgMTMyLjVMMTA1MCAxMzIuNVpNMTE1My41IDEzMkwxMTU5IDEzMS41TDExNjAgMTMyLjVMMTE2NSAxMzIuNUwxMTY2IDEzMy41TDExNjggMTMzLjVMMTE3MiAxMzUuNUwxMTc5LjUgMTQzTDExODIuNSAxNDhMMTE4Mi41IDE1MEwxMTg0LjUgMTU0TDExODQuNSAxNTdMMTE4NS41IDE1OEwxMTg1LjUgMTY2TDExMjQuNSAxNjZMMTEyNC41IDE2MUwxMTI1LjUgMTYwTDExMjYuNSAxNTRMMTEyOS41IDE0OEwxMTM1LjUgMTQxTDExMzUuNSAxNDBMMTE0NSAxMzMuNUwxMTQ3IDEzMy41TDExNDggMTMyLjVMMTE1MyAxMzIuNVpNNjY5LjUgMTM0TDY4MyAxMzMuNUw2ODQgMTM0LjVMNjkxIDEzNi41TDcwMS41IDE0Nkw3MDUuNSAxNTNMNzA1LjUgMTU1TDcwNi41IDE1Nkw3MDYuNSAxNjBMNzA3LjUgMTYxTDcwNy41IDE5MEw3MDYuNSAxOTFMNzA2LjUgMTk2TDcwNS41IDE5N0w3MDUuNSAxOTlMNjk4LjUgMjEwTDY5MyAyMTQuNUw2ODQgMjE4LjVMNjgwIDIxOC41TDY3OSAyMTkuNUw2NjcgMjE4LjVMNjU3IDIxMy41TDY0OS41IDIwNkw2NDQuNSAxOTZMNjQ0LjUgMTk0TDY0My41IDE5M0w2NDMuNSAxODlMNjQyLjUgMTg4TDY0Mi41IDE4MEw2NDEuNSAxNzlMNjQxLjUgMTc1TDY0Mi41IDE3NEw2NDIuNSAxNjZMNjQzLjUgMTY1TDY0My41IDE2MUw2NDQuNSAxNjBMNjQ1LjUgMTU1TDY1MS41IDE0NUw2NTcgMTM5LjVMNjY0IDEzNS41TDY2OSAxMzQuNVpNNDYxLjUgMTc3TDQ3Ny41IDE3N0w0NzcuNSAxOThMNDc2LjUgMTk5TDQ3NS41IDIwNUw0NzEuNSAyMTJMNDY3IDIxNi41TDQ1OCAyMjEuNUw0NTYgMjIxLjVMNDU1IDIyMi41TDQ0MiAyMjIuNUw0MzQgMjE4LjVMNDI4LjUgMjEwTDQyNy41IDIwMEw0MjguNSAxOTlMNDI4LjUgMTk1TDQzMC41IDE5MUw0MzggMTgzLjVMNDQ0IDE4MC41TDQ0NiAxODAuNUw0NTAgMTc4LjVMNDU0IDE3OC41TDQ1NSAxNzcuNUw0NjEgMTc3LjVaTTEzNDEuNSAxNzdMMTM1Ny41IDE3N0wxMzU3LjUgMjAwTDEzNTYuNSAyMDFMMTM1Ni41IDIwNEwxMzUyLjUgMjExTDEzNDMgMjE5LjVMMTMzNiAyMjEuNUwxMzM1IDIyMi41TDEzMjIgMjIyLjVMMTMyMSAyMjEuNUwxMzE5IDIyMS41TDEzMTcgMjE5LjVMMTMxNiAyMTkuNUwxMzA5LjUgMjEyTDEzMDkuNSAyMTBMMTMwOC41IDIwOUwxMzA4LjUgMTk3TDEzMTEuNSAxOTBMMTMxNyAxODQuNUwxMzIyIDE4MS41TDEzMjQgMTgxLjVMMTMyNyAxNzkuNUwxMzM0IDE3OC41TDEzMzUgMTc3LjVMMTM0MSAxNzcuNVpNMTIxOC41IDIwOUwxMjI4IDIwOC41TDEyMzIgMjEwLjVMMTIzNS41IDIxNEwxMjM3LjUgMjE4TDEyMzcuNSAyMjhMMTIzNC41IDIzNEwxMjMwIDIzNy41TDEyMjggMjM3LjVMMTIyNyAyMzguNUwxMjIwIDIzOC41TDEyMTkgMjM3LjVMMTIxNyAyMzcuNUwxMjEyLjUgMjM0TDEyMDkuNSAyMjhMMTIwOS41IDIxOEwxMjExLjUgMjE0TDEyMTUgMjEwLjVMMTIxOCAyMDkuNVpNMTU4Ni41IDIxNkwxNTg3LjUgMjE2TDE1ODcuNSAyMjJMMTU4Ni41IDIyMkwxNTg2LjUgMjE3WiI+PC9wYXRoPjwvc3ZnPg=="
LOGO_HTML = '<img src="data:image/svg+xml;base64,' + LOGO_B64 + '" style="width:100%;max-width:220px;display:block;margin-bottom:4px;">'

st.set_page_config(
    page_title="Review Sentiment Aggregator | OrangeTree Global",
    page_icon="⭐",
    layout="wide",
)

st.markdown("""
<style>
    .header-bar {
        background: linear-gradient(90deg, #F36621, #E05A10);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
    }
    .intro-box {
        background: #fff9f0;
        border: 1px solid #fdd9b5;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .platform-box {
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
    }
    .platform-google { background: #e8f0fe; border-left: 5px solid #4285F4; }
    .platform-zomato { background: #fde8e8; border-left: 5px solid #E23744; }
    .platform-swiggy { background: #fff3e0; border-left: 5px solid #FC8019; }
    .review-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        border: 1px solid #e9ecef;
    }
    .theme-pill {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        border-radius: 12px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .response-box {
        background: #f8fff8;
        border-left: 4px solid #28a745;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-style: italic;
        color: #333;
    }
    .tip-box {
        background: #fffbe6;
        border-left: 4px solid #f0a500;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        font-size: 0.88rem;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<img src="data:image/svg+xml;base64,{LOGO_B64}" style="width:280px;max-width:100%;display:block;margin-bottom:12px;">',
    unsafe_allow_html=True
)
st.markdown("## Review & Sentiment Aggregator")
st.markdown("Paste reviews from Google, Zomato, and Swiggy → get unified sentiment analysis, recurring themes, and ready-to-post responses.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_HTML, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**API Key**")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...",
        help="Get a free key at console.anthropic.com. Used only for this session, never stored.")

    st.markdown("**Model**")
    model = st.selectbox("Model", ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"], index=1)

    st.markdown("---")
    st.markdown("**Your Business**")

    business_name = st.text_input("Business / Restaurant name",
        placeholder="e.g. Bhawanipur House",
        help="Used in the AI-generated responses so they sound personalised to your brand")
    business_type = st.selectbox("What type of business?",
        ["Restaurant / Café", "QSR / Fast Food", "Cloud Kitchen", "Retail Shop", "Salon / Spa", "Clinic / Wellness", "Other"],
        help="Helps Claude understand your context — e.g. delivery complaints are more relevant for a cloud kitchen than a dine-in restaurant")
    tone = st.selectbox("How should responses sound?",
        ["Professional & warm", "Casual & friendly", "Formal", "Apologetic & empathetic"],
        help="Choose the voice that matches your brand. Claude will write all review responses in this tone.")

    st.markdown("---")
    st.markdown("**Demo Data**")
    if st.button("Load Sample Reviews (F&B Demo)", use_container_width=True):
        st.session_state["sample_loaded"] = True
        st.success("Sample reviews loaded! Switch to the review tabs above.")

    st.markdown("---")
    st.info("For best results, paste at least 5–10 reviews per platform.", icon="ℹ️")
    st.caption("UC6 of OrangeTree's AI SME Suite. Powered by Claude API.")

# Sample reviews
SAMPLE_REVIEWS = {
    "google": """5★ - Amazing biriyani, best in the area! The portions are generous and the flavours are authentic. Will come back again. - Arnab D.
4★ - Good food but the waiting time was too long. Took almost 45 minutes on a weekday. Service needs improvement. - Priya M.
2★ - Ordered mutton curry and found it undercooked. Staff was rude when I complained. Very disappointing. - Rajesh K.
5★ - Celebrating my anniversary here was wonderful. Staff made us feel special and the desserts were outstanding! - Moumita S.
3★ - Average experience. The ambience is nice but food quality has gone down compared to last year. - Somnath B.""",
    "zomato": """4.5★ - The Kasha Mangsho is to die for! Highly recommend for Bengali cuisine lovers. Packaging was also good for delivery. - foodie_kolkata
1★ - Order arrived 90 minutes late and was cold. Tried calling the restaurant, no one picked up. Zomato support was useless too. Refund still pending. - AngryCustumer99
5★ - My go-to place for special occasions. The thali gives great value for money. - tasteofkolkata
3★ - Decent food but pricey for the quantity. The restaurant seems to have reduced portions recently. - budget_eater
4★ - Loved the mustard fish! The delivery was on time and food was well-packed. - FoodLover_BHW""",
    "swiggy": """5 stars - Quick delivery and hot food. The chelo chicken is a must-try! Will order again. - Ritu G.
2 stars - Wrong order delivered. Instead of mutton biryani got veg fried rice. Called but no response. Very frustrating. - mango_user_987
4 stars - Consistent quality. Order twice a week from here. Never disappointed with the fish dishes. - regular_customer
3 stars - Food was okay but the chutney was missing from the order. Small thing but still annoying. - NewUser_Kol
5 stars - Best mishti doi in the area! Always order this as a dessert. The quantity has improved since last month too. - sweets_lover"""
}

# ── Review Input ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## Paste Your Reviews")

# Platform explainer
col_g, col_z, col_s = st.columns(3)
with col_g:
    st.markdown("""<div class="platform-box platform-google">
    <b>Google Reviews</b><br>
    <small>Go to Google Maps → search your business → scroll to Reviews → copy and paste them here</small>
    </div>""", unsafe_allow_html=True)
with col_z:
    st.markdown("""<div class="platform-box platform-zomato">
    <b>Zomato Reviews</b><br>
    <small>Open your Zomato restaurant page → Reviews section → copy the text of each review</small>
    </div>""", unsafe_allow_html=True)
with col_s:
    st.markdown("""<div class="platform-box platform-swiggy">
    🟠 <b>Swiggy Reviews</b><br>
    <small>Log into Swiggy Partner app → Ratings & Reviews → copy your customer reviews</small>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="tip-box">
💡 <b>How to paste reviews:</b> You don't need a special format. Just copy-paste the review text as you see it.
Include the star rating if visible (e.g. "4★" or "4 stars"). One review per line works best, but paragraphs are fine too.
You don't need to fill in all three platforms — even one platform's reviews will give you useful insights.
</div>
""", unsafe_allow_html=True)

tab_g, tab_z, tab_s = st.tabs(["Google Reviews", "Zomato Reviews", "Swiggy Reviews"])

default_g = SAMPLE_REVIEWS["google"] if st.session_state.get("sample_loaded") else ""
default_z = SAMPLE_REVIEWS["zomato"] if st.session_state.get("sample_loaded") else ""
default_s = SAMPLE_REVIEWS["swiggy"] if st.session_state.get("sample_loaded") else ""

with tab_g:
    st.markdown("<small style='color:#4285F4'>Paste your Google Maps reviews below. Include as many as you have — the more, the better the analysis.</small>", unsafe_allow_html=True)
    google_reviews = st.text_area("Google Reviews", value=default_g, height=200,
        label_visibility="collapsed",
        placeholder="Paste Google reviews here. Example format:\n5★ - Great food, came back twice! - Arnab D.\n2★ - Service was slow and food was cold. - Priya M.")

with tab_z:
    st.markdown("<small style='color:#E23744'>Paste your Zomato reviews below. Zomato reviews often include delivery feedback — include those too.</small>", unsafe_allow_html=True)
    zomato_reviews = st.text_area("Zomato Reviews", value=default_z, height=200,
        label_visibility="collapsed",
        placeholder="Paste Zomato reviews here...")

with tab_s:
    st.markdown("<small style='color:#FC8019'>Paste your Swiggy reviews below. Delivery time, packaging, and order accuracy complaints often show up here.</small>", unsafe_allow_html=True)
    swiggy_reviews = st.text_area("Swiggy Reviews", value=default_s, height=200,
        label_visibility="collapsed",
        placeholder="Paste Swiggy reviews here...")

# Count reviews entered
total_entered = sum([
    len([l for l in t.split("\n") if l.strip()])
    for t in [google_reviews, zomato_reviews, swiggy_reviews]
    if t.strip()
])

if total_entered > 0:
    st.success(f"✅ {total_entered} review lines detected across platforms. Ready to analyse.", icon="📋")
else:
    st.info("Paste at least a few reviews above to get started. Or load the sample data from the sidebar.", icon="👆")

# Options
st.markdown("---")
st.markdown("#### Analysis options *(optional)*")
col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    date_range = st.selectbox(
        "What time period do these reviews cover?",
        ["Last 7 days", "Last 30 days", "Last 90 days", "Last 6 months", "Last 1 year", "All time"],
        help="This helps Claude contextualise trends — e.g. if you recently changed your menu or processes"
    )
with col_opt2:
    focus = st.multiselect(
        "Any specific areas you want extra focus on?",
        ["Food quality", "Service speed", "Delivery accuracy", "Pricing & value", "Ambience", "Packaging", "Staff behaviour"],
        default=["Food quality", "Service speed", "Delivery accuracy"],
        help="Leave this blank for a general analysis, or select specific topics if you already suspect certain issues"
    )

# ── Analyse ───────────────────────────────────────────────────────────────────
st.markdown("---")
col_b1, col_b2, col_b3 = st.columns([2, 2, 2])
with col_b2:
    analyse_btn = st.button("🔍 Analyse My Reviews", type="primary", use_container_width=True,
                             disabled=(total_entered == 0))

if analyse_btn:
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the left sidebar to continue.")
        st.stop()

    all_reviews_text = ""
    if google_reviews.strip():
        all_reviews_text += f"\n\n=== GOOGLE REVIEWS ===\n{google_reviews.strip()}"
    if zomato_reviews.strip():
        all_reviews_text += f"\n\n=== ZOMATO REVIEWS ===\n{zomato_reviews.strip()}"
    if swiggy_reviews.strip():
        all_reviews_text += f"\n\n=== SWIGGY REVIEWS ===\n{swiggy_reviews.strip()}"

    with st.spinner("Claude is reading every review, identifying patterns, and writing personalised responses..."):
        try:
            client = anthropic.Anthropic(api_key=api_key)

            SYSTEM = """You are a hospitality and SME business intelligence expert. Analyse customer reviews and return a JSON analysis.

Return JSON with this exact structure:
{
  "overall_sentiment": "Positive/Mixed/Negative",
  "overall_score": 0.0-10.0,
  "total_reviews_analysed": number,
  "sentiment_breakdown": {"positive": integer_percent, "neutral": integer_percent, "negative": integer_percent},
  "platform_scores": {
    "Google": {"score": 0.0-10.0, "review_count": number, "one_line_summary": "specific finding"},
    "Zomato": {"score": 0.0-10.0, "review_count": number, "one_line_summary": "specific finding"},
    "Swiggy": {"score": 0.0-10.0, "review_count": number, "one_line_summary": "specific finding"}
  },
  "top_themes": [
    {
      "theme": "Short theme label",
      "sentiment": "positive/negative/mixed",
      "frequency": "High/Medium/Low",
      "what_customers_say": "Plain summary of what customers are actually saying about this",
      "example_quote": "Direct quote from a review",
      "business_impact": "High/Medium/Low"
    }
  ],
  "what_customers_love": [
    {"item": "Specific thing praised", "how_often": "Mentioned in roughly X% of reviews", "why_it_matters": "Keep doing this because..."}
  ],
  "what_needs_fixing": [
    {
      "issue": "Specific complaint in plain English",
      "how_often": "Mentioned in roughly X% of reviews",
      "urgency": "Immediate/Fix Soon/Monitor",
      "real_world_impact": "What this is actually costing you — e.g. lost repeat customers, low ratings",
      "suggested_fix": "Specific, actionable recommendation"
    }
  ],
  "ai_review_responses": [
    {
      "review_excerpt": "First 12-15 words of the review",
      "platform": "Google/Zomato/Swiggy",
      "star_rating": "e.g. 5★ or 2★",
      "sentiment": "positive/negative/neutral",
      "why_respond": "One sentence on why responding to this specific review matters",
      "suggested_response": "Ready-to-post response (2-4 sentences). Make it specific to this review — mention something they actually said. Do NOT use generic phrases like 'We value your feedback'. Sound human."
    }
  ],
  "business_insights": [
    {"insight": "Strategic observation", "what_to_do": "Specific action this insight suggests"}
  ],
  "monthly_priority": "The single most impactful thing to fix this month — written as a clear instruction"
}

For ai_review_responses: generate responses for 4 reviews — the most positive one, the most negative one, one mid-range, and one about delivery/service. Make each response specific to that review's actual content.
Write in the requested tone. Return ONLY valid JSON."""

            USER = f"""Business: {business_name or 'Our Business'}
Type: {business_type}
Review period: {date_range}
Focus areas: {', '.join(focus) if focus else 'General'}
Response tone: {tone}

{all_reviews_text}"""

            response = client.messages.create(
                model=model,
                max_tokens=3500,
                system=SYSTEM,
                messages=[{"role": "user", "content": USER}]
            )

            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            result = json.loads(raw)
            st.session_state["review_result"] = result

        except json.JSONDecodeError as e:
            st.error(f"Response parsing error. Please try again. ({e})")
            st.code(raw)
        except Exception as e:
            st.error(f"API error: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if "review_result" in st.session_state:
    r = st.session_state["review_result"]
    st.markdown("---")
    st.markdown(f"## Review Intelligence Report")
    if business_name:
        st.markdown(f"**{business_name}** &nbsp;|&nbsp; {business_type} &nbsp;|&nbsp; Period: {date_range} &nbsp;|&nbsp; {datetime.now().strftime('%d %B %Y')}")

    st.markdown("""
    <div style="background:#fff9f0; border:1px solid #fdd9b5; border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem; font-size:0.88rem">
    📖 <b>How to read this report:</b> Start with the <b>Overall Score</b> and <b>Monthly Priority</b>.
    Then check <b>What Needs Fixing</b> for the issues hurting your ratings, and copy the <b>AI-Generated Responses</b>
    directly into Google/Zomato/Swiggy. The <b>Strategic Insights</b> section connects review patterns to operational decisions.
    </div>
    """, unsafe_allow_html=True)

    # Top metrics
    overall = r.get("overall_sentiment", "Mixed")
    score = r.get("overall_score", 5)
    score_color = "#28a745" if score >= 7.5 else "#ff8c00" if score >= 5 else "#dc3545"
    total = r.get("total_reviews_analysed", 0)
    breakdown = r.get("sentiment_breakdown", {})
    pos = breakdown.get("positive", 0)
    neu = breakdown.get("neutral", 0)
    neg = breakdown.get("negative", 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Overall Score", f"{score}/10")
        st.markdown(f"<div class='metric-label'>{'Excellent' if score>=8 else 'Good' if score>=7 else 'Needs work' if score>=5 else 'Critical attention needed'}</div>", unsafe_allow_html=True)
    with c2:
        st.metric("Overall Sentiment", overall)
        st.markdown(f"<div class='metric-label'>Across all platforms combined</div>", unsafe_allow_html=True)
    with c3:
        st.metric("Reviews Analysed", total)
        st.markdown(f"<div class='metric-label'>From {sum(1 for x in [google_reviews, zomato_reviews, swiggy_reviews] if x.strip())} platform(s)</div>", unsafe_allow_html=True)
    with c4:
        st.metric("😊 Positive Reviews", f"{pos}%")
        st.markdown(f"<div class='metric-label'>{neg}% negative · {neu}% neutral</div>", unsafe_allow_html=True)

    # Sentiment bar
    st.markdown(f"""
    <b>Sentiment split at a glance:</b>
    <div style="display:flex; height:18px; border-radius:9px; overflow:hidden; margin:8px 0">
        <div style="width:{pos}%; background:#28a745" title="{pos}% Positive"></div>
        <div style="width:{neu}%; background:#ffc107" title="{neu}% Neutral"></div>
        <div style="width:{neg}%; background:#dc3545" title="{neg}% Negative"></div>
    </div>
    <small>🟢 {pos}% positive &nbsp;·&nbsp; 🟡 {neu}% neutral &nbsp;·&nbsp; 🔴 {neg}% negative</small>
    """, unsafe_allow_html=True)

    # Platform breakdown
    st.markdown("---")
    st.markdown("### 📱 How You're Performing on Each Platform")
    st.markdown("<small style='color:#555'>Different platforms attract different types of customers and reviews. Zomato and Swiggy reviews tend to focus on delivery; Google reviews reflect the overall brand experience.</small>", unsafe_allow_html=True)

    platforms = r.get("platform_scores", {})
    pcols = st.columns(max(len(platforms), 1))
    for i, (platform, pdata) in enumerate(platforms.items()):
        with pcols[i]:
            ps = pdata.get("score", 5)
            pcolor = "#28a745" if ps >= 7.5 else "#ff8c00" if ps >= 5 else "#dc3545"
            icon = {"Google": "🔵", "Zomato": "🔴", "Swiggy": "🟠"}.get(platform, "⭐")
            plat_class = platform.lower()
            st.markdown(f"""
            <div class="review-card platform-{plat_class}" style="text-align:center; padding:1rem">
                <div style="font-size:1.2rem">{icon} <b>{platform}</b></div>
                <div style="font-size:2.5rem; font-weight:bold; color:{pcolor}">{ps}/10</div>
                <div style="font-size:0.85rem; color:#555; margin-top:0.3rem">{pdata.get('one_line_summary', '')}</div>
                <div style="font-size:0.8rem; color:#888; margin-top:0.2rem">{pdata.get('review_count', 0)} reviews</div>
            </div>""", unsafe_allow_html=True)

    # What's working vs what needs fixing
    st.markdown("---")
    col_love, col_fix = st.columns(2)

    with col_love:
        st.markdown("### 💚 What's Working — Keep Doing This")
        st.markdown("<small style='color:#555'>These are the things your customers consistently praise. Protecting and promoting these strengths is as important as fixing problems.</small>", unsafe_allow_html=True)
        for item in r.get("what_customers_love", []):
            with st.expander(f"✅ {item.get('item', '')} — {item.get('how_often', '')}"):
                st.markdown(f"**Why this matters:** {item.get('why_it_matters', '')}")

    with col_fix:
        st.markdown("### 🔧 What's Hurting You — Fix These")
        st.markdown("<small style='color:#555'>These are the specific issues driving negative reviews. Each one has a suggested fix — this is your action list.</small>", unsafe_allow_html=True)
        fixes = r.get("what_needs_fixing", [])
        for fix in fixes:
            urgency = fix.get("urgency", "Fix Soon")
            icon = "🚨" if urgency == "Immediate" else "⚠️" if urgency == "Fix Soon" else "👀"
            fix_color = "#dc3545" if urgency == "Immediate" else "#ff8c00" if urgency == "Fix Soon" else "#6c757d"
            with st.expander(f"{icon} {fix.get('issue', '')}"):
                st.markdown(f"**How often this comes up:** {fix.get('how_often', '')}")
                st.markdown(f"**Real-world impact:** {fix.get('real_world_impact', '')}")
                st.markdown(f"**What to do:** {fix.get('suggested_fix', '')}")
                st.markdown(f"<span style='color:{fix_color}; font-weight:bold'>Priority: {urgency}</span>", unsafe_allow_html=True)

    # Themes
    st.markdown("---")
    st.markdown("### 🏷️ Recurring Themes Across All Reviews")
    st.markdown("<small style='color:#555'>These are the topics that keep coming up across all platforms — positive and negative. High-impact themes are the ones most worth acting on.</small>", unsafe_allow_html=True)
    themes = r.get("top_themes", [])
    for theme in themes:
        sentiment = theme.get("sentiment", "mixed")
        s_color = "#28a745" if sentiment == "positive" else "#dc3545" if sentiment == "negative" else "#ff8c00"
        s_icon = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "🟡"
        st.markdown(f"""
        <div class="review-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start">
                <span><span class="theme-pill">{theme.get('theme', '')}</span>
                <span style="color:{s_color}; font-size:0.85rem"> {s_icon} {sentiment.title()} · Frequency: {theme.get('frequency', '')} · Business impact: {theme.get('business_impact', '')}</span></span>
            </div>
            <div style="margin-top:0.5rem; font-size:0.9rem; color:#555">{theme.get('what_customers_say', '')}</div>
            <div style="margin-top:0.4rem; font-size:0.85rem; color:#888">💬 <em>"{theme.get('example_quote', '')}"</em></div>
        </div>""", unsafe_allow_html=True)

    # AI Responses
    st.markdown("---")
    st.markdown("### ✍️ Ready-to-Post Review Responses")
    st.markdown("""
    <small style='color:#555'>
    Responding to reviews — especially negative ones — is one of the highest-ROI activities for your online reputation.
    Businesses that respond to negative reviews see significantly better long-term ratings.
    These responses are written specifically for each review — not generic templates.
    <b>Copy and paste them directly into Google/Zomato/Swiggy.</b>
    </small>
    """, unsafe_allow_html=True)

    responses_list = r.get("ai_review_responses", [])
    for resp in responses_list:
        platform = resp.get("platform", "")
        sentiment = resp.get("sentiment", "neutral")
        rating = resp.get("star_rating", "")
        icon = "🔵" if platform == "Google" else "🔴" if platform == "Zomato" else "🟠"
        s_icon = "😊" if sentiment == "positive" else "😞" if sentiment == "negative" else "😐"

        with st.expander(f"{icon} {platform} {rating} — {s_icon} \"{resp.get('review_excerpt', '')}...\""):
            st.markdown(f"**Why respond to this:** {resp.get('why_respond', '')}")
            st.markdown("**Your response (ready to copy):**")
            st.markdown(f'<div class="response-box">{resp.get("suggested_response", "")}</div>', unsafe_allow_html=True)
            st.code(resp.get("suggested_response", ""), language=None)

    # Strategic insights
    st.markdown("---")
    st.markdown("### 💡 Strategic Business Insights")
    st.markdown("<small style='color:#555'>These go beyond the reviews themselves — they're operational and business decisions implied by the patterns Claude found across all your customer feedback.</small>", unsafe_allow_html=True)
    for insight in r.get("business_insights", []):
        with st.expander(f"💡 {insight.get('insight', '')}"):
            st.markdown(f"**What this suggests you do:** {insight.get('what_to_do', '')}")

    # Monthly priority
    st.markdown("---")
    st.markdown("### 🎯 This Month's #1 Priority")
    st.markdown("<small style='color:#555'>If you could only act on one thing from this entire report, Claude recommends this:</small>", unsafe_allow_html=True)
    priority = r.get("monthly_priority", "")
    if priority:
        st.error(f"**→ {priority}**", icon="🎯")

    # OrangeTree CTA
    st.markdown("""
    <div style="background:#fff9f0; border:1px solid #fdd9b5; border-radius:8px; padding:1rem 1.5rem; margin:1rem 0">
    <h4 style="margin:0 0 0.4rem 0">🌳 Want this running automatically every week?</h4>
    <p style="margin:0; font-size:0.9rem">OrangeTree Global can set up an automated version of this tool — integrated directly with your Google/Zomato/Swiggy accounts —
    that sends you a weekly review digest with responses ready to post. <b>Contact: ssbishnu@gmail.com</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Export
    export_lines = [
        f"REVIEW INTELLIGENCE REPORT — {business_name or 'Your Business'}",
        f"Type: {business_type} | Period: {date_range}",
        f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        "=" * 50,
        f"Overall Score: {score}/10 | Sentiment: {overall}",
        f"Reviews Analysed: {total} | Positive: {pos}% | Neutral: {neu}% | Negative: {neg}%",
        "",
        "WHAT'S WORKING",
        *[f"✅ {item.get('item','')} ({item.get('how_often','')})\n   → {item.get('why_it_matters','')}"
          for item in r.get("what_customers_love", [])],
        "",
        "WHAT NEEDS FIXING",
        *[f"[{f.get('urgency','?')}] {f.get('issue','')}\n   Impact: {f.get('real_world_impact','')}\n   Fix: {f.get('suggested_fix','')}"
          for f in r.get("what_needs_fixing", [])],
        "",
        "READY-TO-POST RESPONSES",
        *[f"\n{resp.get('platform','')} — \"{resp.get('review_excerpt','')}...\"\nResponse: {resp.get('suggested_response','')}"
          for resp in responses_list],
        "",
        "STRATEGIC INSIGHTS",
        *[f"• {i.get('insight','')} → {i.get('what_to_do','')}" for i in r.get("business_insights", [])],
        "",
        f"THIS MONTH'S PRIORITY: {r.get('monthly_priority', '')}",
        "",
        "=" * 50,
        "Generated by OrangeTree Global AI SME Suite — Review Aggregator (UC6)",
    ]

    st.download_button(
        "⬇️ Download Full Report as Text File",
        data="\n".join(export_lines),
        file_name=f"Review_Report_{(business_name or 'Business').replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
    st.caption("OrangeTree Global | AI SME Suite — UC6: Review & Sentiment Aggregator")
