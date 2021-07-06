"""
    Display: Regex & CFG
    Input: any string
    Outputs: (1) "Valid" or "Invalid" checker result based on DFA 
             (2) DFA Simulation of the inputted string
"""
import streamlit as st                          # Library for web app framework (see Streamlit API docu  @ discuss.streamlit.io/t/streamlit-cheat-sheet/4912)
import base64                                   # For rendering SVG to Streamlit (SVG - the DFA file format)
import requests                                 
from visual_automata.fa.dfa import VisualDFA

r1 = "RegEx 1. (bab+bbb)b*a*(a*+b*)(ab)*(aba)(bab+aba)*bb(a+b)*(bab+aba)(a+b)*"
r2 = "RegEx 2. (1+0)*0*1*(111+00+101)(1+0)*(101+01+000)(1+0)*(101+000)*"

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    img = r'<img src="data:image/svg+xml;base64,%s" height="350" width="1750"/>' % b64
    st.write(img, unsafe_allow_html=True)

# Use the full page 
st.set_page_config(layout="wide")
st.title("Deterministic Finite Automaton (DFA) Simulator 🟢🔴🟡")

# Divide page by columns of equal size
c1, c2,c3 = st.beta_columns(3)
  
with c1:    
    st.subheader("① Choose a Regular Expression")
    user_choice = st.selectbox("", [r1, r2])

with c2:
    st.subheader("② Context-Free Grammar ")

st.markdown("---")    
st.markdown("## DFA Simulation")

# Display chosen RegEx
st.text(user_choice)

if user_choice == r1:
    """ Creates DFA represented by a 5-tuple (Q - states, ∑ - input symbols, δ - transitions, q0 - initial state, F - final state) """
    dfa = VisualDFA(
        states={'0', '1', '2','3','4', '5', '6','7','8', '9', '10','11',
       '12', '13', '14','15','16', '17', '18','19','20', '21', '22'},
        input_symbols={"a", "b"},
        transitions={ '0' : {'a' : '1', 'b' : '2'},
            '1' : {'a' : '1', 'b' : '1'},
            '2' : {'a' : '3', 'b' : '3'},
            '3' : {'a' : '1', 'b' : '4'},
            '4' : {'a' : '5', 'b' : '4'},
            '5' : {'a' : '5', 'b' : '6'},
            '6' : {'a' : '7', 'b' : '8'},
            '7' : {'a' : '12', 'b' : '11'},
            '8' : {'a' : '9', 'b' : '8'},
            '9' : {'a' : '1', 'b' : '10'},
            '10' : {'a' : '7', 'b' : '1'},
            '11' : {'a' : '7', 'b' : '16'},
            '12' : {'a' : '1', 'b' : '13'},
            '13' : {'a' : '14', 'b' : '1'},
            '14' : {'a' : '12', 'b' : '15'},
            '15' : {'a' : '17', 'b' : '16'},
            '16' : {'a' : '20', 'b' : '18'},
            '17' : {'a' : '1', 'b' : '14'},
            '18' : {'a' : '19', 'b' : '18'},
            '19' : {'a' : '20', 'b' : '22'},
            '20' : {'a' : '20', 'b' : '21'},
            '21' : {'a' : '22', 'b' : '18'},
            '22' : {'a' : '22', 'b' : '22'}
          },
        initial_state="0",
        final_states={"22"},
        )    

    with c2:
        # Add CFG within an expander
        my_expander = st.beta_expander("Expand", expanded=True)
        with my_expander:
            st.write("S → ABCDEFBGB")
            st.write("A → bab | bbb")
            st.write("B → bB | aB | λ")
            st.write("C → abC | λ") 
            st.write("D → aba")
            st.write("E → babE | abaE | λ")
            st.write("F → bb")
            st.write("G → bab | aba")
  
if user_choice == r2:
    dfa = VisualDFA(
        states={'0', '1', '2', '3', '4', '5','6', '7', '8'},
        input_symbols={"0", "1"},
        transitions= { '0' : {'0' : '1', '1' : '6'},
            '1' : {'0' : '2', '1' : '6'},
            '2' : {'0' : '3', '1' : '2'},
            '3' : {'0' : '4', '1' : '5'},
            '4' : {'0' : '5', '1' : '5'},
            '5' : {'0' : '5', '1' : '5'},
            '6' : {'0' : '7', '1' : '8'},
            '7' : {'0' : '2', '1' : '2'},
            '8' : {'0' : '7', '1' : '2'}
            },
            initial_state="0",
            final_states={"5"},
            )

    with c2:
        my_expander = st.beta_expander("Expand", expanded=True)
        with my_expander:
            st.write("S → ABCDAEAF")
            st.write("A → 0A | 1A | λ")
            st.write("B → 0B | λ")
            st.write("C → 1C | λ")
            st.write("D → 111 | 00 | 101")
            st.write("E → 101 | 01 | 000")
            st.write(" F → 101F | 001F |  λ")

try:
    with c3:
        st.subheader("③  String Checker")
        string = st.text_input("Enter a String below to Simulate Automaton")
        test = st.button('Test')
           
    if test and not string:
        c3.write("You need to enter a string!")         # Error message
    elif user_choice == c1 or c2 and test:
        try: 
            checker = dfa.input_check(string)
            if "[Accepted]" in checker:
                result = "VALID ✅ "
                DFA = dfa.show_diagram(string)
            else:
                result = "INVALID ⭕ "
                DFA = dfa.show_diagram(string)
        except:
            result = "INVALID ⭕ "
        c3.write("**" + result + "**")
                  
   
    # Reformat and save DFA as .svg
    DFA.format = "svg"
    DFA.render("simulation")

    # Open the saved .svg file from local directory
    s = open("simulation.svg","r")
    lines = s.readlines()
    DFA_Final=''.join(lines)

    # Display inputted string
    st.write("Transition graph for string **" + string + "**.")  

    # Display DFA Simulation
    render_svg(DFA_Final)

except:
    st.empty()
    print('Finished...')

