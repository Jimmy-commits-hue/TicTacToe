# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 05:35:49 2026

@author: jabulani Khabana
"""

import streamlit as st
import random

st.title("Tic Tac Toe")

# Instructions
st.write("Player vs Computer")
st.write("Choose a position from 1 to 9")
st.write()

if "human_sign" not in st.session_state:
    st.session_state.human_sign = None

if "computer_sign" not in st.session_state:
    st.session_state.computer_sign = None

# Choose signs
signs = ['X', 'O']

if st.session_state.human_sign is None:
    chosen = st.selectbox("Choose your sign", signs)

    if st.button("Confirm Sign"):
        st.session_state.human_sign = chosen
        st.session_state.computer_sign = 'O' if chosen == 'X' else 'X'
        st.session_state.ready_for_next_play = True
        st.rerun()
else:
    human = st.session_state.human_sign
    computer = st.session_state.computer_sign
    st.write(f"You are playing as **{human}**")


# State
if "board" not in st.session_state:
    st.session_state.board = [' '] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "ready_for_next_play" not in st.session_state:
    st.session_state.ready_for_next_play = True

# Print board
def print_board(board):
    st.text(
        f"""
 {board[0]} | {board[1]} | {board[2]}
-----------
 {board[3]} | {board[4]} | {board[5]}
-----------
 {board[6]} | {board[7]} | {board[8]}
"""
    )

print_board(st.session_state.board)

# Check winner
def check_winner(board, sign):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    return any(board[a] == board[b] == board[c] == sign for a, b, c in wins)

# Player input
move_input = st.text_input("Your move (1 - 9)")

move = None
if move_input.isdigit():
    move = int(move_input)

# Play button
if st.session_state.ready_for_next_play and not st.session_state.game_over:

    if st.button("Play"):
      if move is None or move < 1 or move > 9:
        st.error("Please enter a number between 1 and 9")
      else:
        st.session_state.ready_for_next_play = False
        index = move - 1

        if st.session_state.board[index] != ' ':
            st.error("That position is already taken!")
            st.session_state.ready_for_next_play = True
        else:
            # Human move
            st.session_state.board[index] = human
            print_board(st.session_state.board)

            if check_winner(st.session_state.board, human):
                st.success("You win!")
                st.session_state.game_over = True
                st.session_state.ready_for_next_play = False

# Computer turn
if not st.session_state.ready_for_next_play and not st.session_state.game_over:

    empty_positions = [
        i for i, v in enumerate(st.session_state.board) if v == ' '
    ] 

    if empty_positions:
        comp_move = random.choice(empty_positions)
        st.session_state.board[comp_move] = computer
        st.info("Computer played")
        print_board(st.session_state.board)

        if check_winner(st.session_state.board, computer):
            st.error("Computer wins!")
            st.session_state.game_over = True
        else:
            # Computer finished -> show Play button again
            st.session_state.ready_for_next_play = True
    else:
        st.warning("It's a draw!")
        st.session_state.game_over = True

# Restart
if st.button("Restart Game"):
    st.session_state.board = [' '] * 9
    st.session_state.game_over = False
    st.session_state.ready_for_next_play = True
    st.session_state.human_sign = None
    st.session_state.computer_sign = None

