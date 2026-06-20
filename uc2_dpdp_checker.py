"""
OrangeTree Global — DPDP Readiness & Data Risk Checker (UC2)
Digital Personal Data Protection Act 2023 (India)
Powered by Claude API (Anthropic)
Run: streamlit run uc2_dpdp_checker.py
"""

import streamlit as st
import anthropic
import json
from datetime import datetime

# -- Embedded logo (base64) so no separate SVG file needed on Streamlit Cloud --
LOGO_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjUgOSAxNTg2IDI2OCIgd2lkdGg9IjE1ODYiIGhlaWdodD0iMjY4Ij48dGl0bGU+T3JhbmdlVHJlZS57YWl9PC90aXRsZT48cGF0aCBmaWxsPSIjMUE3QTMwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xODIuNSAxM0wxODMuNSAxM0wxODMuNSAxOEwxODIuNSAxOUwxODIuNSAyMkwxODEuNSAyM0wxODAuNSAyOEwxNzguNSAzMUwxNzguNSAzM0wxNzMuNSA0M0wxNzEuNSA0NUwxNjcuNSA1MkwxNjMuNSA1NkwxNjMuNSA1N0wxNTMgNjcuNUwxNTIgNjcuNUwxNDUgNzMuNUwxNDIgNzQuNUwxNDAgNzYuNUwxMzYgNzguNUwxMzQgNzguNUwxMzAgODAuNUwxMjcgODAuNUwxMjYgODEuNUwxMTYgODEuNUwxMTUgODAuNUwxMTIgODAuNUwxMDUgNzYuNUwxMDAuNSA3MkwxMDAuNSA3MUwxMDYgNjguNUwxMDggNjYuNUwxMTUgNjIuNUwxMTggNTkuNUwxMTkgNTkuNUwxMjQgNTQuNUwxMjUgNTQuNUwxMzEuNSA0OEwxMzEuNSA0N0wxMzAgNDYuNUwxMTUgNTQuNUwxMTMgNTQuNUwxMDkgNTYuNUwxMDYgNTYuNUwxMDUgNTcuNUw5NiA1Ny41TDk1IDU2LjVMOTMgNTYuNUw4OC41IDUxTDg4LjUgNDRMOTIuNSAzNUw5NS41IDMyTDk1LjUgMzFMMTAzIDI0LjVMMTEyIDIwLjVMMTE5IDIwLjVMMTIwIDE5LjVMMTQ4IDE5LjVMMTQ5IDE4LjVMMTU5IDE4LjVMMTYwIDE3LjVMMTY2IDE3LjVMMTY3IDE2LjVMMTcxIDE2LjVMMTcyIDE1LjVMMTc1IDE1LjVMMTc2IDE0LjVMMTgyIDEzLjVaTTI5LjUgMTdMMzAgMTYuNUwzNCAyMC41TDM1IDIwLjVMNDAgMjQuNUw1MiAzMC41TDU0IDMwLjVMNjMgMzUuNUw2NSAzNS41TDY3IDM3LjVMNzIgMzkuNUw3NSA0Mi41TDc2IDQyLjVMODIuNSA1MEw4Mi41IDUyTDg0LjUgNTZMODQuNSA2MEw4MyA2MS41TDc3IDYyLjVMNzYgNjMuNUw2OCA2My41TDY3IDY0LjVMNjYgNjMuNUw1OSA2My41TDU4IDYyLjVMNTUgNjIuNUw0NiA1Ny41TDM4LjUgNDlMMzQuNSA0MUwzMy41IDM1TDMyLjUgMzRMMzIuNSAzMUwzMS41IDMwTDMxLjUgMjRMMzAuNSAyM0wzMCAxNy41Wk0xMzEuNSA0NkwxMzIgNDUuNUwxMzIgNDYuNVoiPjwvcGF0aD48cGF0aCBmaWxsPSIjRjM2NjIxIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik05My41IDg3TDExOSA4Ni41TDEyMCA4Ny41TDEyNCA4Ny41TDEyNSA4OC41TDEzMyA5MC41TDE0MyA5NS41TDE0NSA5Ny41TDE1MiAxMDEuNUwxNTYgMTA1LjVMMTU3IDEwNS41TDE2Ni41IDExNUwxNjYuNSAxMTZMMTcwLjUgMTIwTDE3MC41IDEyMUwxNzMuNSAxMjRMMTc0LjUgMTI3TDE3Ni41IDEyOUwxODEuNSAxMzlMMTgxLjUgMTQxTDE4Mi41IDE0MkwxODIuNSAxNDRMMTg1LjUgMTUxTDE4NS41IDE1NEwxODYuNSAxNTVMMTg2LjUgMTYwTDE4Ny41IDE2MUwxODcuNSAxODFMMTg2LjUgMTgyTDE4Ni41IDE4OEwxODUuNSAxODlMMTg1LjUgMTkzTDE4My41IDE5N0wxODIuNSAyMDNMMTc5LjUgMjA4TDE3OS41IDIxMEwxNzcuNSAyMTRMMTc1LjUgMjE2TDE3NC41IDIxOUwxNjcuNSAyMjhMMTY3LjUgMjI5TDE1NSAyNDEuNUwxNTQgMjQxLjVMMTUxIDI0NC41TDE1MCAyNDQuNUwxNDUgMjQ4LjVMMTQyIDI0OS41TDE0MCAyNTEuNUwxMzYgMjUzLjVMMTM0IDI1My41TDEyOSAyNTYuNUwxMjMgMjU3LjVMMTE5IDI1OS41TDExNSAyNTkuNUwxMTQgMjYwLjVMMTA4IDI2MC41TDEwNyAyNjEuNUw4OSAyNjEuNUw4OCAyNjAuNUw4MiAyNjAuNUw4MSAyNTkuNUw3MyAyNTguNUw3MiAyNTcuNUw2NyAyNTYuNUw2NCAyNTQuNUw2MiAyNTQuNUw1MiAyNDkuNUw0MyAyNDIuNUw0MiAyNDIuNUwyNi41IDIyN0wyNi41IDIyNkwyMC41IDIxOEwxMi41IDIwMUwxMS41IDE5NUwxMC41IDE5NEwxMC41IDE5MUw5LjUgMTkwTDkuNSAxODVMOC41IDE4NEw4LjUgMTYyTDkuNSAxNjFMMTAuNSAxNTNMMTEuNSAxNTJMMTMuNSAxNDRMMTYuNSAxMzhMMTguNSAxMzZMMjEuNSAxMzBMMzEgMTE5LjVMMzEuNSAxMjBMMjQuNSAxMzNMMjQuNSAxMzVMMjEuNSAxNDJMMjEuNSAxNTVMMjQuNSAxNjFMMzAgMTY1LjVMMzYgMTY4LjVMNDQgMTY5LjVMNDUgMTcwLjVMNzEgMTcwLjVMNzIgMTY5LjVMNzYgMTY5LjVMNzcgMTY4LjVMODAgMTY4LjVMODEgMTY3LjVMODkgMTY1LjVMMTA1IDE1Ny41TDEwNyAxNTUuNUwxMTQgMTUxLjVMMTMxLjUgMTM1TDEzMS41IDEzNEwxMzYuNSAxMjhMMTQwLjUgMTE5TDE0MC41IDEwOUwxMzguNSAxMDVMMTMyIDk4LjVMMTI0IDk0LjVMMTIwIDk0LjVMMTE5IDkzLjVMMTA0IDkzLjVMMTAzIDk0LjVMOTUgOTUuNUw5NCA5Ni41TDg5IDk3LjVMODQgMTAwLjVMODIgMTAwLjVMODAgMTAyLjVMNzcgMTAzLjVMNzEgMTA4LjVMNzAgMTA4LjVMNjAuNSAxMThMNjAuNSAxMTlMNTcuNSAxMjJMNTYuNSAxMjVMNTQuNSAxMjdMNTQuNSAxMjlMNTIuNSAxMzNMNTIuNSAxNDFMNTQuNSAxNDVMNTcgMTQ3LjVMNjMgMTUwLjVMNzQgMTUwLjVMNzUgMTQ5LjVMNzkgMTQ4LjVMODQuNSAxNDNMODUuNSAxNDFMODUuNSAxMzNMODQuNSAxMzJMODMuNSAxMjdMNzcuNSAxMTlMODUgMTE0LjVMODcgMTE0LjVMOTMgMTExLjVMOTYgMTExLjVMOTcgMTEwLjVMMTExIDExMC41TDExNy41IDExNkwxMTcuNSAxMThMMTE4LjUgMTE5TDExOC41IDEyNEwxMTcuNSAxMjVMMTE3LjUgMTI4TDExMi41IDEzN0wxMDMgMTQ2LjVMOTAgMTU0LjVMODggMTU0LjVMODUgMTU2LjVMODMgMTU2LjVMNzkgMTU4LjVMNzYgMTU4LjVMNzUgMTU5LjVMNzAgMTU5LjVMNjkgMTYwLjVMNTMgMTYwLjVMNTIgMTU5LjVMNDggMTU5LjVMNDcgMTU4LjVMNDIgMTU3LjVMMzUgMTUzLjVMMzAuNSAxNDhMMzAuNSAxNDZMMjguNSAxNDJMMjguNSAxMzZMMjkuNSAxMzVMMjkuNSAxMzFMMzQuNSAxMjFMMzcuNSAxMThMMzcuNSAxMTdMNDcgMTA3LjVMNDggMTA3LjVMNTIgMTAzLjVMNTMgMTAzLjVMNTggOTkuNUw3MiA5Mi41TDc0IDkyLjVMNzUgOTEuNUw3NyA5MS41TDg0IDg4LjVMODcgODguNUw4OCA4Ny41TDkzIDg3LjVaIj48L3BhdGg+PHBhdGggZmlsbD0iIzAwMDAwMCIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMjcwLjUgNzFMMjc3IDcwLjVMMjc4IDcxLjVMMjg3IDcxLjVMMjg4IDcyLjVMMjkyIDcyLjVMMjk2IDc0LjVMMjk5IDc0LjVMMzAyIDc2LjVMMzA0IDc2LjVMMzEwIDc5LjVMMzE5IDg2LjVMMzIwIDg2LjVMMzI4LjUgOTVMMzI4LjUgOTZMMzMzLjUgMTAyTDMzNC41IDEwNUwzMzYuNSAxMDdMMzM5LjUgMTEzTDMzOS41IDExNUwzNDEuNSAxMThMMzQyLjUgMTI0TDM0NC41IDEyOEwzNDUuNSAxMzhMMzQ2LjUgMTM5TDM0Ni41IDE2OEwzNDUuNSAxNjlMMzQ0LjUgMTc5TDM0My41IDE4MEwzNDMuNSAxODNMMzQyLjUgMTg0TDM0MC41IDE5MkwzMzguNSAxOTVMMzM4LjUgMTk3TDMzNi41IDIwMUwzMzQuNSAyMDNMMzMzLjUgMjA2TDMyOC41IDIxMkwzMjguNSAyMTNMMzE1IDIyNS41TDMxNCAyMjUuNUwzMDkgMjI5LjVMMzAzIDIzMi41TDMwMSAyMzIuNUwyOTggMjM0LjVMMjkyIDIzNS41TDI5MSAyMzYuNUwyODggMjM2LjVMMjg3IDIzNy41TDI4MSAyMzcuNUwyODAgMjM4LjVMMjYzIDIzOC41TDI2MiAyMzcuNUwyNTcgMjM3LjVMMjU2IDIzNi41TDI0OSAyMzUuNUwyNDEgMjMxLjVMMjM5IDIzMS41TDIzNyAyMjkuNUwyMzQgMjI4LjVMMjMyIDIyNi41TDIyOCAyMjQuNUwyMTMuNSAyMDlMMjEwLjUgMjAzTDIwOC41IDIwMUwyMDcuNSAxOTdMMjA0LjUgMTkyTDIwNC41IDE5MEwyMDIuNSAxODZMMjAyLjUgMTgzTDIwMS41IDE4MkwyMDEuNSAxNzlMMjAwLjUgMTc4TDIwMC41IDE3M0wxOTkuNSAxNzJMMTk4LjUgMTUwTDE5OS41IDE0OUwxOTkuNSAxNDBMMjAwLjUgMTM5TDIwMC41IDEzNEwyMDEuNSAxMzNMMjAyLjUgMTI2TDIwMy41IDEyNUwyMDQuNSAxMjBMMjA2LjUgMTE3TDIwNi41IDExNUwyMTAuNSAxMDdMMjEyLjUgMTA1TDIxNi41IDk4TDIyOSA4NS41TDIzMCA4NS41TDIzOCA3OS41TDI0MiA3Ny41TDI0NCA3Ny41TDI0NyA3NS41TDI1MiA3NC41TDI1MyA3My41TDI2MSA3Mi41TDI2MiA3MS41TDI3MCA3MS41Wk0xMjgyLjUgNzFMMTI5MC41IDcxTDEyOTAuNSA4NEwxMjgwIDg0LjVMMTI3OSA4NS41TDEyNzcgODUuNUwxMjcwLjUgOTFMMTI2OC41IDk1TDEyNjguNSA5N0wxMjY3LjUgOThMMTI2Ny41IDExNEwxMjY4LjUgMTE1TDEyNjguNSAxMjFMMTI2OS41IDEyMkwxMjY5LjUgMTI4TDEyNzAuNSAxMjlMMTI3MC41IDE0OUwxMjY5LjUgMTUwTDEyNjguNSAxNTVMMTI2Ni41IDE1N0wxMjY2LjUgMTU4TDEyNjEgMTYzLjVMMTI1NyAxNjUuNUwxMjU1IDE2NS41TDEyNTQuNSAxNjdMMTI2MSAxNjkuNUwxMjY2LjUgMTc1TDEyNjkuNSAxODFMMTI2OS41IDE4NEwxMjcwLjUgMTg1TDEyNzAuNSAyMDVMMTI2OS41IDIwNkwxMjY4LjUgMjE5TDEyNjcuNSAyMjBMMTI2Ny41IDIzNUwxMjY4LjUgMjM2TDEyNjguNSAyMzlMMTI3MC41IDI0M0wxMjc0IDI0Ni41TDEyODEgMjQ5LjVMMTI5MC41IDI1MEwxMjkwLjUgMjYyTDEyNzYgMjYyLjVMMTI3NSAyNjEuNUwxMjY5IDI2MC41TDEyNjMgMjU3LjVMMTI1NS41IDI1MEwxMjUyLjUgMjQ0TDEyNTIuNSAyNDJMMTI1MS41IDI0MUwxMjUxLjUgMjM2TDEyNTAuNSAyMzVMMTI1MS41IDIxNUwxMjUyLjUgMjE0TDEyNTIuNSAyMDhMMTI1My41IDIwN0wxMjUzLjUgMjAxTDEyNTQuNSAyMDBMMTI1NC41IDE4NUwxMjUzLjUgMTg0TDEyNTIuNSAxODBMMTI0OCAxNzUuNUwxMjQ0IDE3NC41TDEyNDMgMTczLjVMMTIzOSAxNzMuNUwxMjM1LjUgMTcyTDEyMzUuNSAxNjFMMTI0NCAxNTkuNUwxMjUwIDE1Ni41TDEyNTEuNSAxNTVMMTI1NC41IDE0OEwxMjU0LjUgMTMzTDEyNTMuNSAxMzJMMTI1My41IDEyNUwxMjUyLjUgMTI0TDEyNTEuNSAxMTBMMTI1MC41IDEwOUwxMjUwLjUgOThMMTI1MS41IDk3TDEyNTIuNSA4OUwxMjU2LjUgODJMMTI2NCA3NS41TDEyNzEgNzIuNUwxMjc0IDcyLjVMMTI3NSA3MS41TDEyODIgNzEuNVpNMTQyMC41IDcxTDE0MjggNzAuNUwxNDI5IDcxLjVMMTQzNiA3MS41TDE0MzcgNzIuNUwxNDQzIDczLjVMMTQ1MCA3Ny41TDE0NTUuNSA4M0wxNDU4LjUgODlMMTQ1OS41IDk1TDE0NjAuNSA5NkwxNDYwLjUgMTEyTDE0NTkuNSAxMTNMMTQ1OS41IDEyMEwxNDU4LjUgMTIxTDE0NTcuNSAxMzZMMTQ1Ni41IDEzN0wxNDU2LjUgMTQ2TDE0NTcuNSAxNDdMMTQ1Ny41IDE1MUwxNDYzIDE1Ny41TDE0NjcgMTU5LjVMMTQ3Ni41IDE2MUwxNDc2LjUgMTcyTDE0NzMgMTcyLjVMMTQ3MiAxNzMuNUwxNDY4IDE3My41TDE0NjIgMTc2LjVMMTQ1OC41IDE4MUwxNDU3LjUgMTgzTDE0NTcuNSAxODZMMTQ1Ni41IDE4N0wxNDU3LjUgMjA1TDE0NTguNSAyMDZMMTQ1OS41IDIyMEwxNDYwLjUgMjIxTDE0NjAuNSAyMzdMMTQ1OS41IDIzOEwxNDU5LjUgMjQyTDE0NTYuNSAyNDlMMTQ1MSAyNTUuNUwxNDUwIDI1NS41TDE0NDUgMjU5LjVMMTQ0MyAyNTkuNUwxNDM5IDI2MS41TDE0MzYgMjYxLjVMMTQzNSAyNjIuNUwxNDIwLjUgMjYyTDE0MjAuNSAyNTBMMTQzMCAyNDkuNUwxNDMxIDI0OC41TDE0MzMgMjQ4LjVMMTQzNyAyNDYuNUwxNDQwLjUgMjQzTDE0NDIuNSAyMzlMMTQ0Mi41IDIzN0wxNDQzLjUgMjM2TDE0NDMuNSAyMThMMTQ0Mi41IDIxN0wxNDQyLjUgMjEwTDE0NDEuNSAyMDlMMTQ0MS41IDIwNEwxNDQwLjUgMjAzTDE0NDAuNSAxODZMMTQ0MS41IDE4NUwxNDQyLjUgMTc5TDE0NDUuNSAxNzRMMTQ1MiAxNjguNUwxNDU2LjUgMTY3TDE0NTYgMTY1LjVMMTQ1MiAxNjQuNUwxNDQ1LjUgMTU5TDE0NDIuNSAxNTRMMTQ0Mi41IDE1MkwxNDQwLjUgMTQ4TDE0NDAuNSAxMzFMMTQ0MS41IDEzMEwxNDQxLjUgMTI0TDE0NDIuNSAxMjNMMTQ0Mi41IDExN0wxNDQzLjUgMTE2TDE0NDMuNSA5N0wxNDQyLjUgOTZMMTQ0Mi41IDk0TDE0NDEuNSA5MkwxNDM2IDg2LjVMMTQzNCA4NS41TDE0MzIgODUuNUwxNDMxIDg0LjVMMTQyMSA4NC41TDE0MjAuNSA3MlpNMTU4NC41IDczTDE1ODcuNSA3M0wxNTg3IDkxLjVMMTU4Ni41IDgzTDE1ODUuNSA4MkwxNTg1LjUgNzZMMTU4NC41IDc0Wk04MjkuNSA3NEw5NDkuNSA3NEw5NDkgOTEuNUw5MDAuNSA5Mkw5MDAgMjM1LjVMODc5LjUgMjM1TDg3OS41IDkyTDgzMCA5MS41TDgyOS41IDc1Wk0xNDAwLjUgNzRMMTQwOCA3My41TDE0MDkgNzQuNUwxNDExIDc0LjVMMTQxNi41IDgwTDE0MTYuNSA4MkwxNDE3LjUgODNMMTQxNy41IDkxTDE0MTYuNSA5M0wxNDExIDk4LjVMMTQwOSA5OC41TDE0MDggOTkuNUwxNDAxIDk5LjVMMTQwMCA5OC41TDEzOTggOTguNUwxMzkyLjUgOTNMMTM5Mi41IDkxTDEzOTEuNSA5MEwxMzkxLjUgODNMMTM5Mi41IDgyTDEzOTIuNSA4MEwxMzk4IDc0LjVMMTQwMCA3NC41Wk0yNjMuNSA4OUwyODIgODguNUwyODMgODkuNUwyODYgODkuNUwyODcgOTAuNUwyODkgOTAuNUwyOTYgOTMuNUwzMDIgOTguNUwzMDMgOTguNUwzMDguNSAxMDRMMzA4LjUgMTA1TDMxNS41IDExNEwzMTguNSAxMjBMMzE4LjUgMTIyTDMxOS41IDEyM0wzMTkuNSAxMjVMMzIyLjUgMTMyTDMyMy41IDE0MkwzMjQuNSAxNDNMMzI0LjUgMTY2TDMyMy41IDE2N0wzMjMuNSAxNzJMMzIyLjUgMTczTDMyMi41IDE3N0wzMjEuNSAxNzhMMzIwLjUgMTg0TDMxOC41IDE4N0wzMTguNSAxODlMMzE0LjUgMTk3TDMxMi41IDE5OUwzMTAuNSAyMDNMMzAxIDIxMi41TDI5MyAyMTcuNUwyOTEgMjE3LjVMMjg4IDIxOS41TDI4NSAyMTkuNUwyODQgMjIwLjVMMjgwIDIyMC41TDI3OSAyMjEuNUwyNjcgMjIxLjVMMjY2IDIyMC41TDI2MiAyMjAuNUwyNjEgMjE5LjVMMjU4IDIxOS41TDI1NSAyMTcuNUwyNTMgMjE3LjVMMjQ1IDIxMi41TDIzNS41IDIwM0wyMjYuNSAxODdMMjI2LjUgMTg1TDIyNC41IDE4MUwyMjQuNSAxNzhMMjIzLjUgMTc3TDIyMy41IDE3NEwyMjIuNSAxNzNMMjIyLjUgMTY4TDIyMS41IDE2N0wyMjEuNSAxNDRMMjIyLjUgMTQzTDIyMi41IDEzN0wyMjMuNSAxMzZMMjIzLjUgMTMzTDIyNC41IDEzMkwyMjQuNSAxMjlMMjI1LjUgMTI4TDIyNy41IDEyMEwyMzMuNSAxMDlMMjQ0IDk3LjVMMjU0IDkxLjVMMjU2IDkxLjVMMjYwIDg5LjVMMjYzIDg5LjVaTTQwMi41IDExN0w0MTAgMTE2LjVMNDEyLjUgMTE4TDQxMi41IDEzN0w0MTEgMTM3LjVMNDEwIDEzNi41TDQwMiAxMzYuNUw0MDEgMTM3LjVMMzk4IDEzNy41TDM5MSAxNDAuNUwzODEuNSAxNTFMMzc5LjUgMTU1TDM3OC41IDE2MEwzNzcuNSAxNjFMMzc3LjUgMTY0TDM3Ni41IDE2NUwzNzYuNSAyMzVMMzU1LjUgMjM1TDM1NS41IDEzNUwzNTQuNSAxMzRMMzU0LjUgMTIwTDM3Mi41IDEyMEwzNzIuNSAxMjVMMzczLjUgMTI2TDM3NCAxNDIuNUwzODAuNSAxMzBMMzg4IDEyMi41TDM5NSAxMTguNUwzOTcgMTE4LjVMMzk4IDExNy41TDQwMiAxMTcuNVpNNDQ2LjUgMTE3TDQ2MCAxMTYuNUw0NjEgMTE3LjVMNDY2IDExNy41TDQ2NyAxMTguNUw0NzMgMTE5LjVMNDc5IDEyMi41TDQ4OC41IDEzMUw0OTQuNSAxNDJMNDk1LjUgMTQ4TDQ5Ni41IDE0OUw0OTYuNSAxNTRMNDk3LjUgMTU1TDQ5Ny41IDIyM0w0OTguNSAyMjRMNDk4LjUgMjMzTDQ5OS41IDIzNUw0ODEgMjM1LjVMNDc5LjUgMjM0TDQ3OS41IDIyNkw0NzguNSAyMjVMNDc4IDIyMS41TDQ2OSAyMzAuNUw0NjAgMjM1LjVMNDU4IDIzNS41TDQ1NCAyMzcuNUw0NTAgMjM3LjVMNDQ5IDIzOC41TDQzNiAyMzguNUw0MzUgMjM3LjVMNDMxIDIzNy41TDQzMCAyMzYuNUw0MjggMjM2LjVMNDE5IDIzMS41TDQxMy41IDIyNkw0MDguNSAyMTdMNDA3LjUgMjExTDQwNi41IDIxMEw0MDYuNSAyMDBMNDA3LjUgMTk5TDQwNy41IDE5NUw0MDguNSAxOTRMNDEwLjUgMTg3TDQxMi41IDE4NUw0MTQuNSAxODFMNDE5IDE3Ni41TDQyMCAxNzYuNUw0MjYgMTcxLjVMNDMyIDE2OC41TDQzNCAxNjguNUw0MzcgMTY2LjVMNDQwIDE2Ni41TDQ0NCAxNjQuNUw0NTQgMTYzLjVMNDU1IDE2Mi41TDQ2NCAxNjIuNUw0NjUgMTYxLjVMNDc2LjUgMTYxTDQ3Ni41IDE1Mkw0NzUuNSAxNTFMNDc1LjUgMTQ4TDQ3Mi41IDE0Mkw0NjcgMTM2LjVMNDYxIDEzMy41TDQ1OCAxMzMuNUw0NTcgMTMyLjVMNDQyIDEzMi41TDQ0MSAxMzMuNUw0MzcgMTMzLjVMNDM2IDEzNC41TDQyOCAxMzYuNUw0MjEgMTQwLjVMNDE5LjUgMTQwTDQxNy41IDEzM0w0MTYuNSAxMzJMNDE2LjUgMTMwTDQxNS41IDEyOUw0MTUuNSAxMjdMNDE3IDEyNS41TDQzMSAxMTkuNUw0MzQgMTE5LjVMNDM1IDExOC41TDQzOCAxMTguNUw0MzkgMTE3LjVMNDQ2IDExNy41Wk01NjUuNSAxMTdMNTc2IDExNi41TDU3NyAxMTcuNUw1ODIgMTE3LjVMNTg4IDEyMC41TDU5MCAxMjAuNUw1OTIgMTIyLjVMNTk1IDEyMy41TDYwMy41IDEzMkw2MDkuNSAxNDNMNjA5LjUgMTQ2TDYxMS41IDE1MEw2MTEuNSAxNTVMNjEyLjUgMTU2TDYxMi41IDIzNUw1OTEuNSAyMzVMNTkxLjUgMTYyTDU5MC41IDE2MUw1OTAuNSAxNTZMNTg5LjUgMTU1TDU4OS41IDE1Mkw1ODUuNSAxNDRMNTc3IDEzNi41TDU3NSAxMzYuNUw1NzEgMTM0LjVMNTU5IDEzNC41TDU1OCAxMzUuNUw1NTUgMTM1LjVMNTQ5IDEzOC41TDUzOS41IDE0OEw1MzYuNSAxNTRMNTM2LjUgMTU2TDUzNS41IDE1N0w1MzUuNSAxNjJMNTM0LjUgMTYzTDUzNC41IDIzNUw1MTMuNSAyMzVMNTEzLjUgMTI1TDUxMi41IDEyNEw1MTIuNSAxMjBMNTMxIDExOS41TDUzMyAxMzguNUw1MzUuNSAxMzRMNTQ1IDEyNC41TDU0NiAxMjQuNUw1NDggMTIyLjVMNTU3IDExOC41TDU2NSAxMTcuNVpNNjY3LjUgMTE3TDY3OCAxMTYuNUw2NzkgMTE3LjVMNjg0IDExNy41TDY4NSAxMTguNUw2ODggMTE4LjVMNjk4IDEyMy41TDcwNi41IDEzMkw3MDkgMTM2LjVMNzA5LjUgMTMwTDcxMC41IDEyOUw3MTEgMTE5LjVMNzI5LjUgMTIwTDcyOS41IDEyM0w3MjguNSAxMjRMNzI4LjUgMjI4TDcyNy41IDIyOUw3MjcuNSAyMzlMNzI2LjUgMjQwTDcyNS41IDI0OUw3MjQuNSAyNTBMNzIzLjUgMjU1TDcxNy41IDI2Nkw3MDggMjc1LjVMNzA2IDI3Ni41TDYzMC41IDI3Nkw2MzEuNSAyNzVMNjMxLjUgMjczTDYzMi41IDI3Mkw2MzIuNSAyNzBMNjMzLjUgMjY5TDYzMy41IDI2N0w2MzQuNSAyNjZMNjM2IDI2MC41TDY0MyAyNjQuNUw2NDUgMjY0LjVMNjUyIDI2Ny41TDY1NSAyNjcuNUw2NTYgMjY4LjVMNjYxIDI2OC41TDY2MiAyNjkuNUw2NzcgMjY5LjVMNjc4IDI2OC41TDY4MiAyNjguNUw2ODMgMjY3LjVMNjg4IDI2Ni41TDY5OC41IDI1OUw3MDQuNSAyNDlMNzA1LjUgMjQzTDcwNi41IDI0Mkw3MDYuNSAyMzhMNzA3LjUgMjM3TDcwNyAyMTYuNUw3MDUuNSAyMTlMNjk3IDIyNy41TDY4OCAyMzIuNUw2ODIgMjMzLjVMNjgxIDIzNC41TDY3NyAyMzQuNUw2NzYgMjM1LjVMNjY1IDIzNS41TDY2NCAyMzQuNUw2NTkgMjM0LjVMNjQ1IDIyOC41TDY0MyAyMjYuNUw2NDIgMjI2LjVMNjMyLjUgMjE3TDYzMi41IDIxNkw2MjkuNSAyMTNMNjI0LjUgMjAzTDYyNC41IDIwMUw2MjIuNSAxOTdMNjIyLjUgMTk0TDYyMS41IDE5M0w2MjEuNSAxODhMNjIwLjUgMTg3TDYyMC41IDE2OUw2MjEuNSAxNjhMNjIxLjUgMTYzTDYyMi41IDE2Mkw2MjMuNSAxNTVMNjI5LjUgMTQyTDYzMS41IDE0MEw2MzMuNSAxMzZMNjQzIDEyNi41TDY0NCAxMjYuNUw2NDkgMTIyLjVMNjUzIDEyMC41TDY2MSAxMTguNUw2NjIgMTE3LjVMNjY3IDExNy41Wk03ODUuNSAxMTdMNzk3IDExNi41TDc5OCAxMTcuNUw4MDMgMTE3LjVMODA0IDExOC41TDgxMCAxMTkuNUw4MTkgMTI0LjVMODI4LjUgMTM0TDgzMy41IDE0Mkw4MzMuNSAxNDRMODM1LjUgMTQ3TDgzNS41IDE0OUw4MzcuNSAxNTNMODM4LjUgMTYzTDgzOS41IDE2NEw4MzkuNSAxNzhMODM4IDE4MS41TDc1OCAxODEuNUw3NTcuNSAxOTBMNzU4LjUgMTkxTDc1OC41IDE5NUw3NTkuNSAxOTZMNzU5LjUgMTk4TDc2NS41IDIwOUw3NzAgMjEzLjVMNzcxIDIxMy41TDc3NiAyMTcuNUw3ODMgMjE5LjVMNzg0IDIyMC41TDc4NyAyMjAuNUw3ODggMjIxLjVMODEwIDIyMS41TDgxMSAyMjAuNUw4MTYgMjIwLjVMODE3IDIxOS41TDgyMCAyMTkuNUw4MjEgMjE4LjVMODI2IDIxNy41TDgyOSAyMTUuNUw4MjkuNSAyMTlMODMwLjUgMjIwTDgzMC41IDIyM0w4MzEuNSAyMjRMODMxLjUgMjI3TDgzMi41IDIyOEw4MzIuNSAyMzFMODMwIDIzMi41TDgyMiAyMzQuNUw4MjEgMjM1LjVMODE3IDIzNS41TDgxNiAyMzYuNUw4MTIgMjM2LjVMODExIDIzNy41TDgwMiAyMzcuNUw4MDEgMjM4LjVMNzg4IDIzOC41TDc4NyAyMzcuNUw3ODEgMjM3LjVMNzgwIDIzNi41TDc3NyAyMzYuNUw3NzYgMjM1LjVMNzcwIDIzNC41TDc1OSAyMjguNUw3NTAuNSAyMjFMNzUwLjUgMjIwTDc0Ni41IDIxNkw3NDUuNSAyMTNMNzQyLjUgMjA5TDc0Mi41IDIwN0w3NDAuNSAyMDRMNzQwLjUgMjAyTDczOC41IDE5OEw3MzguNSAxOTRMNzM3LjUgMTkzTDczNy41IDE4Nkw3MzYuNSAxODVMNzM2LjUgMTc0TDczNy41IDE3M0w3MzcuNSAxNjZMNzM4LjUgMTY1TDczOC41IDE2MUw3MzkuNSAxNjBMNzM5LjUgMTU3TDc0MC41IDE1Nkw3NDEuNSAxNTFMNzQ4LjUgMTM4TDc1My41IDEzM0w3NTMuNSAxMzJMNzYxIDEyNS41TDc3MCAxMjAuNUw3NzIgMTIwLjVMNzc5IDExNy41TDc4NSAxMTcuNVpNOTk1LjUgMTE3TDEwMDQgMTE2LjVMMTAwNi41IDExOEwxMDA2LjUgMTM3TDEwMDUgMTM3LjVMMTAwNCAxMzYuNUw5OTYgMTM2LjVMOTk1IDEzNy41TDk5MSAxMzcuNUw5ODUgMTQwLjVMOTc5LjUgMTQ1TDk3OS41IDE0Nkw5NzYuNSAxNDlMOTczLjUgMTU0TDk3My41IDE1Nkw5NzEuNSAxNjBMOTcxLjUgMTYzTDk3MC41IDE2NEw5NzAuNSAxNzBMOTY5LjUgMTcxTDk2OS41IDIzNUw5NDguNSAyMzVMOTQ4LjUgMTIwTDk2Ni41IDEyMEw5NjYuNSAxMzNMOTY3LjUgMTM0TDk2OCAxNDIuNUw5NjguNSAxNDBMOTczLjUgMTMxTDk4MiAxMjIuNUw5ODkgMTE4LjVMOTk1IDExNy41Wk0xMDQ5LjUgMTE3TDEwNjIgMTE2LjVMMTA2MyAxMTcuNUwxMDY4IDExNy41TDEwNjkgMTE4LjVMMTA3NCAxMTkuNUwxMDgyIDEyMy41TDEwODUgMTI2LjVMMTA4NiAxMjYuNUwxMDkzLjUgMTM1TDEwOTkuNSAxNDZMMTA5OS41IDE0OEwxMTAxLjUgMTUyTDExMDEuNSAxNTVMMTEwMi41IDE1NkwxMTAyLjUgMTYwTDExMDMuNSAxNjFMMTEwNCAxNjkuNUwxMTA2LjUgMTU2TDExMTEuNSAxNDRMMTExMy41IDE0MkwxMTE0LjUgMTM5TDExMTcuNSAxMzZMMTExNy41IDEzNUwxMTI5IDEyNC41TDExMzkgMTE5LjVMMTE0NSAxMTguNUwxMTQ2IDExNy41TDExNTEgMTE3LjVMMTE1MiAxMTYuNUwxMTY0IDExNi41TDExNjUgMTE3LjVMMTE3MCAxMTcuNUwxMTcxIDExOC41TDExNzQgMTE4LjVMMTE3NyAxMjAuNUwxMTgxIDEyMS41TDExODMgMTIzLjVMMTE4NyAxMjUuNUwxMTk0LjUgMTMzTDExOTQuNSAxMzRMMTE5OC41IDEzOUwxMjAxLjUgMTQ1TDEyMDEuNSAxNDdMMTIwNC41IDE1NEwxMjA0LjUgMTU4TDEyMDUuNSAxNTlMMTIwNS41IDE2N0wxMjA2LjUgMTY4TDEyMDYuNSAxNzVMMTIwNS41IDE3NkwxMjA1IDE4MS41TDExMjQgMTgxLjVMMTEyMy41IDE4NkwxMTI0LjUgMTg3TDExMjQuNSAxOTJMMTEyNS41IDE5M0wxMTI1LjUgMTk2TDExMjkuNSAyMDVMMTEzMS41IDIwN0wxMTMxLjUgMjA4TDExNDEgMjE2LjVMMTE0NyAyMTkuNUwxMTQ5IDIxOS41TDExNTAgMjIwLjVMMTE1NCAyMjAuNUwxMTU1IDIyMS41TDExNzcgMjIxLjVMMTE3OCAyMjAuNUwxMTgyIDIyMC41TDExODMgMjE5LjVMMTE5MCAyMTguNUwxMTkzIDIxNi41TDExOTYgMjE2LjVMMTE5OS41IDIzMUwxMTkxIDIzNC41TDExODggMjM0LjVMMTE4NyAyMzUuNUwxMTg0IDIzNS41TDExODMgMjM2LjVMMTE3OSAyMzYuNUwxMTc4IDIzNy41TDExNjkgMjM3LjVMMTE2OCAyMzguNUwxMTU1IDIzOC41TDExNTQgMjM3LjVMMTE0MyAyMzYuNUwxMTQyIDIzNS41TDExMzcgMjM0LjVMMTEyNyAyMjkuNUwxMTE1LjUgMjE5TDExMTUuNSAyMThMMTExMS41IDIxM0wxMTA1LjUgMTk5TDExMDUuNSAxOTVMMTEwNC41IDE5NEwxMTA0LjUgMTg5TDExMDMuNSAxODhMMTEwMyAxODEuNUwxMDIxLjUgMTgyTDEwMjEuNSAxODlMMTAyMi41IDE5MEwxMDIyLjUgMTk0TDEwMjMuNSAxOTVMMTAyNC41IDIwMEwxMDI4LjUgMjA3TDEwMzcgMjE1LjVMMTA0NSAyMTkuNUwxMDUxIDIyMC41TDEwNTIgMjIxLjVMMTA3NCAyMjEuNUwxMDc1IDIyMC41TDEwODAgMjIwLjVMMTA4MSAyMTkuNUwxMDg0IDIxOS41TDEwODUgMjE4LjVMMTA5MyAyMTYuNUwxMDk0LjUgMjE5TDEwOTQuNSAyMjJMMTA5NS41IDIyM0wxMDk1LjUgMjI2TDEwOTYuNSAyMjdMMTA5NiAyMzEuNUwxMDg5IDIzNC41TDEwODYgMjM0LjVMMTA4NSAyMzUuNUwxMDgyIDIzNS41TDEwODEgMjM2LjVMMTA3NiAyMzYuNUwxMDc1IDIzNy41TDEwNjcgMjM3LjVMMTA2NiAyMzguNUwxMDUzIDIzOC41TDEwNTIgMjM3LjVMMTA0NSAyMzcuNUwxMDQ0IDIzNi41TDEwNDEgMjM2LjVMMTA0MCAyMzUuNUwxMDMyIDIzMy41TDEwMjIgMjI3LjVMMTAxMi41IDIxOEwxMDEyLjUgMjE3TDEwMDguNSAyMTJMMTAwMy41IDIwMEwxMDAyLjUgMTkyTDEwMDEuNSAxOTFMMTAwMS41IDE2N0wxMDAyLjUgMTY2TDEwMDIuNSAxNjJMMTAwMy41IDE2MUwxMDAzLjUgMTU4TDEwMDQuNSAxNTdMMTAwNS41IDE1MkwxMDExLjUgMTQwTDEwMjQgMTI2LjVMMTAzNCAxMjAuNUwxMDM2IDEyMC41TDEwNDAgMTE4LjVMMTA0MyAxMTguNUwxMDQ0IDExNy41TDEwNDkgMTE3LjVaTTEzMjYuNSAxMTdMMTM0MCAxMTYuNUwxMzQxIDExNy41TDEzNDYgMTE3LjVMMTM0NyAxMTguNUwxMzUwIDExOC41TDEzNTEgMTE5LjVMMTM1NiAxMjAuNUwxMzY2LjUgMTI4TDEzNjYuNSAxMjlMMTM3MC41IDEzM0wxMzc0LjUgMTQxTDEzNzUuNSAxNDdMMTM3Ni41IDE0OEwxMzc2LjUgMTUyTDEzNzcuNSAxNTNMMTM3Ny41IDIxNEwxMzc4LjUgMjE1TDEzNzguNSAyMzBMMTM3OS41IDIzMUwxMzc5LjUgMjM1TDEzNjEgMjM1LjVMMTM2MC41IDIzMUwxMzU5LjUgMjMwTDEzNTkuNSAyMjJMMTM1OCAyMjEuNUwxMzU2LjUgMjI0TDEzNDggMjMxLjVMMTM0MCAyMzUuNUwxMzM4IDIzNS41TDEzMzQgMjM3LjVMMTMzMCAyMzcuNUwxMzI5IDIzOC41TDEzMTYgMjM4LjVMMTMxNSAyMzcuNUwxMzEyIDIzNy41TDEzMTEgMjM2LjVMMTMwNiAyMzUuNUwxMzAxIDIzMi41TDEyOTUuNSAyMjhMMTI5NS41IDIyN0wxMjkyLjUgMjI0TDEyODkuNSAyMTlMMTI4OS41IDIxN0wxMjg3LjUgMjEzTDEyODcuNSAxOTdMMTI4OC41IDE5NkwxMjg4LjUgMTkzTDEyOTMuNSAxODNMMTMwMiAxNzQuNUwxMzE1IDE2Ny41TDEzMTcgMTY3LjVMMTMyMSAxNjUuNUwxMzI0IDE2NS41TDEzMjUgMTY0LjVMMTMyOCAxNjQuNUwxMzI5IDE2My41TDEzNTYuNSAxNjFMMTM1Ni41IDE1MUwxMzU1LjUgMTUwTDEzNTUuNSAxNDdMMTM1MC41IDEzOUwxMzQ0IDEzNC41TDEzNDIgMTM0LjVMMTMzOCAxMzIuNUwxMzIyIDEzMi41TDEzMjEgMTMzLjVMMTMxNyAxMzMuNUwxMzE2IDEzNC41TDEzMDggMTM2LjVMMTMwNCAxMzguNUwxMzAyIDE0MC41TDEyOTkuNSAxNDBMMTI5OS41IDEzOEwxMjk4LjUgMTM3TDEyOTguNSAxMzVMMTI5NS41IDEyOEwxMjk2IDEyNi41TDEzMDMgMTIyLjVMMTMwNSAxMjIuNUwxMzExIDExOS41TDEzMTkgMTE4LjVMMTMyMCAxMTcuNUwxMzI2IDExNy41Wk0xMzkzLjUgMTIwTDE0MTUuNSAxMjBMMTQxNSAyMzUuNUwxMzkzLjUgMjM1TDEzOTMuNSAxMjFaTTc4Ni41IDEzMkw3OTMgMTMxLjVMNzk0IDEzMi41TDc5OCAxMzIuNUw4MDggMTM3LjVMODExLjUgMTQxTDgxNi41IDE1MEw4MTYuNSAxNTJMODE4LjUgMTU2TDgxOC41IDE2NEw4MTkuNSAxNjVMODE4IDE2Ni41TDc1OCAxNjYuNUw3NTcuNSAxNjNMNzU4LjUgMTYyTDc1OC41IDE1OUw3NTkuNSAxNThMNzYwLjUgMTUzTDc2NS41IDE0NEw3NzMgMTM2LjVMNzgyIDEzMi41TDc4NiAxMzIuNVpNMTA1MC41IDEzMkwxMDU3IDEzMS41TDEwNTggMTMyLjVMMTA2MiAxMzIuNUwxMDYzIDEzMy41TDEwNjUgMTMzLjVMMTA3MSAxMzYuNUwxMDc2LjUgMTQyTDEwODAuNSAxNDlMMTA4MC41IDE1MUwxMDgyLjUgMTU1TDEwODMuNSAxNjZMMTAyMiAxNjYuNUwxMDIxLjUgMTY0TDEwMjIuNSAxNjNMMTAyMi41IDE1OUwxMDIzLjUgMTU4TDEwMjMuNSAxNTZMMTAyNS41IDE1M0wxMDI2LjUgMTQ5TDEwMjguNSAxNDdMMTAzMC41IDE0M0wxMDM5IDEzNS41TDEwNDYgMTMyLjVMMTA1MCAxMzIuNVpNMTE1My41IDEzMkwxMTU5IDEzMS41TDExNjAgMTMyLjVMMTE2NSAxMzIuNUwxMTY2IDEzMy41TDExNjggMTMzLjVMMTE3MiAxMzUuNUwxMTc5LjUgMTQzTDExODIuNSAxNDhMMTE4Mi41IDE1MEwxMTg0LjUgMTU0TDExODQuNSAxNTdMMTE4NS41IDE1OEwxMTg1LjUgMTY2TDExMjQuNSAxNjZMMTEyNC41IDE2MUwxMTI1LjUgMTYwTDExMjYuNSAxNTRMMTEyOS41IDE0OEwxMTM1LjUgMTQxTDExMzUuNSAxNDBMMTE0NSAxMzMuNUwxMTQ3IDEzMy41TDExNDggMTMyLjVMMTE1MyAxMzIuNVpNNjY5LjUgMTM0TDY4MyAxMzMuNUw2ODQgMTM0LjVMNjkxIDEzNi41TDcwMS41IDE0Nkw3MDUuNSAxNTNMNzA1LjUgMTU1TDcwNi41IDE1Nkw3MDYuNSAxNjBMNzA3LjUgMTYxTDcwNy41IDE5MEw3MDYuNSAxOTFMNzA2LjUgMTk2TDcwNS41IDE5N0w3MDUuNSAxOTlMNjk4LjUgMjEwTDY5MyAyMTQuNUw2ODQgMjE4LjVMNjgwIDIxOC41TDY3OSAyMTkuNUw2NjcgMjE4LjVMNjU3IDIxMy41TDY0OS41IDIwNkw2NDQuNSAxOTZMNjQ0LjUgMTk0TDY0My41IDE5M0w2NDMuNSAxODlMNjQyLjUgMTg4TDY0Mi41IDE4MEw2NDEuNSAxNzlMNjQxLjUgMTc1TDY0Mi41IDE3NEw2NDIuNSAxNjZMNjQzLjUgMTY1TDY0My41IDE2MUw2NDQuNSAxNjBMNjQ1LjUgMTU1TDY1MS41IDE0NUw2NTcgMTM5LjVMNjY0IDEzNS41TDY2OSAxMzQuNVpNNDYxLjUgMTc3TDQ3Ny41IDE3N0w0NzcuNSAxOThMNDc2LjUgMTk5TDQ3NS41IDIwNUw0NzEuNSAyMTJMNDY3IDIxNi41TDQ1OCAyMjEuNUw0NTYgMjIxLjVMNDU1IDIyMi41TDQ0MiAyMjIuNUw0MzQgMjE4LjVMNDI4LjUgMjEwTDQyNy41IDIwMEw0MjguNSAxOTlMNDI4LjUgMTk1TDQzMC41IDE5MUw0MzggMTgzLjVMNDQ0IDE4MC41TDQ0NiAxODAuNUw0NTAgMTc4LjVMNDU0IDE3OC41TDQ1NSAxNzcuNUw0NjEgMTc3LjVaTTEzNDEuNSAxNzdMMTM1Ny41IDE3N0wxMzU3LjUgMjAwTDEzNTYuNSAyMDFMMTM1Ni41IDIwNEwxMzUyLjUgMjExTDEzNDMgMjE5LjVMMTMzNiAyMjEuNUwxMzM1IDIyMi41TDEzMjIgMjIyLjVMMTMyMSAyMjEuNUwxMzE5IDIyMS41TDEzMTcgMjE5LjVMMTMxNiAyMTkuNUwxMzA5LjUgMjEyTDEzMDkuNSAyMTBMMTMwOC41IDIwOUwxMzA4LjUgMTk3TDEzMTEuNSAxOTBMMTMxNyAxODQuNUwxMzIyIDE4MS41TDEzMjQgMTgxLjVMMTMyNyAxNzkuNUwxMzM0IDE3OC41TDEzMzUgMTc3LjVMMTM0MSAxNzcuNVpNMTIxOC41IDIwOUwxMjI4IDIwOC41TDEyMzIgMjEwLjVMMTIzNS41IDIxNEwxMjM3LjUgMjE4TDEyMzcuNSAyMjhMMTIzNC41IDIzNEwxMjMwIDIzNy41TDEyMjggMjM3LjVMMTIyNyAyMzguNUwxMjIwIDIzOC41TDEyMTkgMjM3LjVMMTIxNyAyMzcuNUwxMjEyLjUgMjM0TDEyMDkuNSAyMjhMMTIwOS41IDIxOEwxMjExLjUgMjE0TDEyMTUgMjEwLjVMMTIxOCAyMDkuNVpNMTU4Ni41IDIxNkwxNTg3LjUgMjE2TDE1ODcuNSAyMjJMMTU4Ni41IDIyMkwxNTg2LjUgMjE3WiI+PC9wYXRoPjwvc3ZnPg=="
LOGO_HTML = '<img src="data:image/svg+xml;base64,' + LOGO_B64 + '" style="width:100%;max-width:220px;display:block;margin-bottom:4px;">'

st.set_page_config(
    page_title="DPDP Readiness Checker | OrangeTree Global",
    page_icon="🌳",
    layout="wide",
)

st.markdown("""
<style>
    .header-bar {
        background: linear-gradient(90deg, #F36621, #E05A10);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .section-divider {
        border-left: 4px solid #F36621;
        padding: 0.4rem 0.8rem;
        background: #fff3ee;
        border-radius: 4px;
        margin: 1.5rem 0 0.6rem 0;
        font-weight: bold;
        font-size: 0.95rem;
    }
    .result-card {
        background: #f8f9fa;
        border-left: 4px solid #F36621;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        margin: 0.4rem 0;
    }
    .score-box {
        text-align: center;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        background: #fff3ee;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<img src="data:image/svg+xml;base64,{LOGO_B64}" style="width:280px;max-width:100%;display:block;margin-bottom:12px;">',
    unsafe_allow_html=True
)
st.markdown("## DPDP Readiness Checker")
st.markdown("Answer 16 questions about your data practices → get a compliance score, gap analysis and action plan under India's DPDP Act 2023")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_HTML, unsafe_allow_html=True)
    st.markdown("---")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Get a free key at console.anthropic.com. Used only for this session — never stored."
    )
    model = st.selectbox(
        "Model",
        ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        index=1,
        help="claude-sonnet is the best balance of speed and depth"
    )
    st.markdown("---")
    st.markdown("**Your Organisation**")
    org_name = st.text_input("Organisation name", placeholder="e.g. Bhawanipur House")
    org_type = st.selectbox("Sector", [
        "F&B / Restaurant", "Retail", "Healthcare / Clinic", "Education / EdTech",
        "Financial Services / NBFC", "Manufacturing", "IT / SaaS", "HR / Staffing", "Other"
    ], help="Different sectors have different data risk profiles under DPDP")
    org_size = st.selectbox("Number of employees", ["1–10", "11–50", "51–200", "200+"])
    st.markdown("---")
    st.markdown("**About this tool**")
    st.info("UC2 of OrangeTree's AI SME Suite. Powered by Claude API.", icon="ℹ️")
    st.caption("Preliminary self-assessment only. Not legal advice.")

# ── Intro ─────────────────────────────────────────────────────────────────────
st.markdown("""
India's **DPDP Act 2023** applies to any business that collects, stores or processes personal data —
including customer names, phone numbers, emails, and purchase history.
Answer each question based on your **current** practices. There are no wrong answers — this is a diagnostic, not a test.
""")

# ── Questionnaire ─────────────────────────────────────────────────────────────
OPTIONS = ["Yes — fully in place", "Partially — work in progress", "No — not done yet", "Not applicable"]
responses = {}

# Pillar 1
st.markdown('<div class="section-divider">Pillar 1 — Consent</div>', unsafe_allow_html=True)
responses["p1_q1"] = st.radio("Do you get explicit consent before collecting personal data?", OPTIONS, key="p1q1", horizontal=True,
    help="Name, phone, email, purchase history — anything that identifies a person. A signup form alone isn't enough; users must actively agree.")
responses["p1_q2"] = st.radio("Can customers withdraw consent and opt out easily?", OPTIONS, key="p1q2", horizontal=True,
    help="Withdrawing consent must be as easy as giving it. A buried unsubscribe link may not be sufficient under DPDP.")
responses["p1_q3"] = st.radio("Do you have a written Privacy Notice visible at the point of data collection?", OPTIONS, key="p1q3", horizontal=True,
    help="Tells customers what data you collect, why, and how. Must be visible before they share data — not just in your website footer.")

# Pillar 2
st.markdown('<div class="section-divider">Pillar 2 — Data Minimisation</div>', unsafe_allow_html=True)
responses["p2_q1"] = st.radio("Do you collect only the data you actually use — nothing extra 'just in case'?", OPTIONS, key="p2q1", horizontal=True,
    help="Example: a restaurant needs a phone for reservations but not a date of birth. Collecting unused data is a DPDP risk.")
responses["p2_q2"] = st.radio("Is data used only for the purpose it was originally collected for?", OPTIONS, key="p2q2", horizontal=True,
    help="Using a delivery phone number for WhatsApp marketing requires separate consent. Repurposing data without fresh consent is a violation.")
responses["p2_q3"] = st.radio("Do you have a register listing what personal data you hold, where it is stored, and why?", OPTIONS, key="p2q3", horizontal=True,
    help="Even a simple spreadsheet counts. This is one of the first things a regulator or DPDP audit will ask for.")

# Pillar 3
st.markdown('<div class="section-divider">Pillar 3 — Customer Rights</div>', unsafe_allow_html=True)
responses["p3_q1"] = st.radio("Can a customer ask 'what data do you have on me?' and get a clear answer?", OPTIONS, key="p3q1", horizontal=True,
    help="If data is scattered across WhatsApp, Excel sheets, and a CRM, this is very hard to fulfil. DPDP requires you to be able to respond.")
responses["p3_q2"] = st.radio("Can customers request correction or deletion of their data?", OPTIONS, key="p3q2", horizontal=True,
    help="Right to Correction and Right to Erasure. A contact email or form is the minimum required process.")
responses["p3_q3"] = st.radio("Do you have a process to respond to these requests within a reasonable timeframe?", OPTIONS, key="p3q3", horizontal=True,
    help="Having the right is only useful if someone processes the request. Is there a named owner and a response timeline in your business?")

# Pillar 4
st.markdown('<div class="section-divider">Pillar 4 — Internal Accountability</div>', unsafe_allow_html=True)
responses["p4_q1"] = st.radio("Is someone in your organisation responsible for data protection compliance?", OPTIONS, key="p4q1", horizontal=True,
    help="Doesn't need to be a formal Data Protection Officer. But someone must own it — otherwise penalties fall on the business owner.")
responses["p4_q2"] = st.radio("Do you have a process to detect, contain and report a data breach?", OPTIONS, key="p4q2", horizontal=True,
    help="If your CRM is hacked or a laptop with customer data is stolen, DPDP requires you to notify the Data Protection Board and affected customers.")
responses["p4_q3"] = st.radio("Do vendor contracts (apps, delivery platforms, payment gateways) include data protection clauses?", OPTIONS, key="p4q3", horizontal=True,
    help="When you share customer data with third parties like Zomato or Razorpay, you remain legally responsible for how they handle it.")

# Pillar 5
st.markdown('<div class="section-divider">Pillar 5 — Sensitive and Children\'s Data</div>', unsafe_allow_html=True)
responses["p5_q1"] = st.radio("If under-18s use your service, do you have age verification and parental consent?", OPTIONS, key="p5q1", horizontal=True,
    help="DPDP's strictest rules apply to minors. If your service could be used by someone under 18, this applies — even if you don't target children.")
responses["p5_q2"] = st.radio("Is sensitive data (health, financial, biometric) held with extra security measures?", OPTIONS, key="p5q2", horizontal=True,
    help="Examples: clinic patient records, salary data, dietary restrictions, biometric attendance data. These require stronger encryption and tighter access controls.")

# Pillar 6
st.markdown('<div class="section-divider">Pillar 6 — Security and Cross-Border Data</div>', unsafe_allow_html=True)
responses["p6_q1"] = st.radio("Is customer data stored securely with restricted access and password protection?", OPTIONS, key="p6q1", horizontal=True,
    help="Includes Google Sheets (who has the link?), CRM (shared passwords?), WhatsApp groups, email inboxes. Only the right people should have access.")
responses["p6_q2"] = st.radio("Does your customer data leave India — stored on foreign cloud servers or foreign SaaS tools?", OPTIONS, key="p6q2", horizontal=True,
    help="Google Workspace, AWS, Mailchimp, HubSpot may store data outside India. DPDP has specific cross-border transfer rules — one of the most overlooked SME risks.")
responses["p6_q3"] = st.radio("Are employee access logs to customer data tracked?", OPTIONS, key="p6q3", horizontal=True,
    help="If an employee leaks customer data, can you detect it? Knowing which team members can access your CRM or spreadsheet is a starting point.")

# Optional context
st.markdown("---")
additional_context = st.text_area(
    "Additional context (optional)",
    placeholder="e.g. We use WhatsApp, Tally, Zoho CRM, Google Sheets. We collect CCTV footage. 3 staff have database access...",
    help="More context gives Claude more targeted advice"
)

# Progress + Submit
answered = sum(1 for v in responses.values() if v)
st.markdown(f"**{answered} / 16 questions answered**")

col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    analyse_btn = st.button("Generate DPDP Report", type="primary",
                             use_container_width=True, disabled=(answered < 16))

if answered < 16:
    st.info(f"{16 - answered} question(s) remaining above.")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyse_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
        st.stop()

    score_map = {
        "Yes — fully in place": 3,
        "Partially — work in progress": 1.5,
        "No — not done yet": 0,
        "Not applicable": 3
    }
    applicable = {k: v for k, v in responses.items() if v != "Not applicable"}
    total_possible = len(applicable) * 3
    total_score = sum(score_map.get(v, 0) for v in applicable.values())
    raw_pct = int((total_score / total_possible) * 100) if total_possible > 0 else 0

    with st.spinner("Analysing your compliance posture across all 6 DPDP pillars..."):
        try:
            client = anthropic.Anthropic(api_key=api_key)
            responses_text = "\n".join([f"- {k}: {v}" for k, v in responses.items()])

            SYSTEM = """You are an expert in India's Digital Personal Data Protection Act 2023.
Return a JSON object with this exact structure:
{
  "overall_risk": "High/Medium/Low",
  "compliance_summary": "2-3 sentences in plain English for an SME owner. No jargon. What does this score mean for their business?",
  "pillar_scores": {
    "Consent": {"score": 0-100, "status": "Compliant/Partial/Non-compliant", "finding": "one practical sentence"},
    "Data Minimisation": {"score": 0-100, "status": "...", "finding": "..."},
    "Customer Rights": {"score": 0-100, "status": "...", "finding": "..."},
    "Accountability": {"score": 0-100, "status": "...", "finding": "..."},
    "Sensitive Data": {"score": 0-100, "status": "...", "finding": "..."},
    "Security": {"score": 0-100, "status": "...", "finding": "..."}
  },
  "critical_gaps": [
    {
      "gap": "Plain-English description",
      "why_it_matters": "Real consequence if not fixed",
      "action": "Specific step to take",
      "effort": "This week / 1-2 weeks / 1-3 months"
    }
  ],
  "quick_wins": ["Action phrased as an instruction, completable this week at no cost"],
  "penalty_risk": "Plain-English summary of fine exposure with rupee figures where applicable",
  "next_steps": ["Step 1 with named owner", "Step 2", "Step 3"]
}
Specific to DPDP Act 2023 (India), not GDPR. Return ONLY valid JSON."""

            USER = f"""Organisation: {org_name or 'Unknown'} | Sector: {org_type} | Size: {org_size}
Additional context: {additional_context or 'None'}
Raw score: {raw_pct}%

Responses:
{responses_text}"""

            response = client.messages.create(
                model=model, max_tokens=2500, system=SYSTEM,
                messages=[{"role": "user", "content": USER}]
            )

            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            result = json.loads(raw)
            result["raw_pct"] = raw_pct
            st.session_state["dpdp_result"] = result

        except json.JSONDecodeError as e:
            st.error(f"Parsing error: {e}. Please try again.")
            st.code(raw)
        except Exception as e:
            st.error(f"API error: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if "dpdp_result" in st.session_state:
    r = st.session_state["dpdp_result"]
    st.markdown("---")
    st.markdown(f"## DPDP Compliance Report — {org_name or 'Your Organisation'}")
    st.caption(f"Generated {datetime.now().strftime('%d %B %Y, %H:%M')} | Preliminary self-assessment only — not legal advice")

    # Score row
    score = r.get("raw_pct", 0)
    risk  = r.get("overall_risk", "Medium")
    risk_color = {"High": "#dc3545", "Medium": "#F36621", "Low": "#28a745"}.get(risk, "#F36621")
    risk_bg    = {"High": "#fff3f3", "Medium": "#fff3ee", "Low": "#f0fff4"}.get(risk, "#fff3ee")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:3rem; font-weight:bold; color:{risk_color}">{score}%</div>
            <div style="color:#555; font-size:0.9rem">Compliance Score</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:1.6rem; font-weight:bold; color:{risk_color}">{risk} Risk</div>
            <div style="color:#555; font-size:0.85rem; margin-top:0.3rem">Overall exposure level</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        gaps = len(r.get("critical_gaps", []))
        st.markdown(f"""<div class="score-box">
            <div style="font-size:3rem; font-weight:bold; color:#F36621">{gaps}</div>
            <div style="color:#555; font-size:0.9rem">Critical Gaps Found</div>
        </div>""", unsafe_allow_html=True)

    st.info(r.get("compliance_summary", ""))

    # Pillar scores
    st.markdown('<div class="section-divider">Pillar Breakdown</div>', unsafe_allow_html=True)
    for name, data in r.get("pillar_scores", {}).items():
        ps = data.get("score", 50)
        status = data.get("status", "Partial")
        bar_color = "#28a745" if ps >= 70 else "#F36621" if ps >= 40 else "#dc3545"
        icon = "✓" if ps >= 70 else "~" if ps >= 40 else "✗"
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px">
                <b>{name}</b>
                <span style="color:{bar_color}; font-size:0.9rem">{icon} {status} ({ps}%)</span>
            </div>
            <div style="background:#e9ecef; border-radius:4px; height:6px; margin-bottom:6px">
                <div style="background:{bar_color}; width:{ps}%; height:6px; border-radius:4px"></div>
            </div>
            <small style="color:#555">{data.get('finding', '')}</small>
        </div>""", unsafe_allow_html=True)

    # Critical gaps
    st.markdown('<div class="section-divider">Critical Gaps</div>', unsafe_allow_html=True)
    for i, gap in enumerate(r.get("critical_gaps", []), 1):
        effort = gap.get("effort", "")
        effort_color = "#dc3545" if "month" in effort.lower() else "#F36621" if "week" in effort.lower() else "#28a745"
        with st.expander(f"Gap {i} — {gap.get('gap', '')}"):
            st.markdown(f"**Why it matters:** {gap.get('why_it_matters', '')}")
            st.markdown(f"**What to do:** {gap.get('action', '')}")
            st.markdown(f"**Effort:** <span style='color:{effort_color}; font-weight:bold'>{effort}</span>", unsafe_allow_html=True)

    # Quick wins
    st.markdown('<div class="section-divider">Quick Wins — Do These This Week</div>', unsafe_allow_html=True)
    for qw in r.get("quick_wins", []):
        st.markdown(f"— {qw}")

    # Penalty exposure
    st.markdown('<div class="section-divider">Penalty Exposure</div>', unsafe_allow_html=True)
    st.warning(r.get("penalty_risk", ""))

    # Action plan
    st.markdown('<div class="section-divider">Your Action Plan</div>', unsafe_allow_html=True)
    for i, ns in enumerate(r.get("next_steps", []), 1):
        st.markdown(f"**{i}.** {ns}")

    # Export
    st.markdown("---")
    export_text = f"""DPDP COMPLIANCE REPORT
Organisation: {org_name or 'Unknown'} | Sector: {org_type} | Size: {org_size}
Date: {datetime.now().strftime('%d %B %Y')} | Score: {score}% | Risk: {risk}

SUMMARY
{r.get('compliance_summary', '')}

CRITICAL GAPS
""" + "\n".join([
        f"\nGap {i}: {g.get('gap', '')}\n  Why: {g.get('why_it_matters', '')}\n  Action: {g.get('action', '')}\n  Effort: {g.get('effort', '')}"
        for i, g in enumerate(r.get("critical_gaps", []), 1)
    ]) + "\n\nQUICK WINS\n" + "\n".join([f"- {q}" for q in r.get("quick_wins", [])]) + f"""

PENALTY EXPOSURE
{r.get('penalty_risk', '')}

ACTION PLAN
""" + "\n".join([f"{i}. {ns}" for i, ns in enumerate(r.get("next_steps", []), 1)]) + """

Generated by OrangeTree Global AI SME Suite — UC2: DPDP Readiness Checker
DISCLAIMER: Preliminary self-assessment only. Not legal advice.
"""
    col_dl1, col_dl2 = st.columns([1, 3])
    with col_dl1:
        st.download_button(
            "Download Report",
            data=export_text,
            file_name=f"DPDP_Report_{(org_name or 'Org').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    st.caption("OrangeTree Global | AI SME Suite — UC2: DPDP Readiness Checker | Not legal advice.")
