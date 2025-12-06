import spacy
import sys
import time

# --- added a typing effect, because it looks better ---
def type_writer(text, speed=0.04):
    """
    Prints text one character at a time to simulate typing.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Forces the character to show up immediately
        time.sleep(speed)
    print() # Add a line break at the end

# --- loading spacy library ---
# need the 'lg' (large) model here or the vectors are not very good
print("🧠 Booting up the brain (Loading spaCy)...")
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("Error: Model not found. Run 'python -m spacy download en_core_web_lg'")
    exit()

def organize_items(items, categories):
    # --- creating empty buckets for the sorting ---
    buckets = {cat: [] for cat in categories}
    
    type_writer("\n🤔 Thinking hard...", speed=0.05)
    
    for item_text in items:
        item_doc = nlp(item_text)
        
        # --- skipping words the model doesn't know, otherwise it crashes/gives 0 score ---
        if not item_doc.has_vector:
            print(f"[?] I don't know what '{item_text}' is. Skipping.")
            continue

        best_score = -1
        best_category = None
        
        # --- comparing the item to every category ---
        for cat in categories:
            cat_doc = nlp(cat)
            
            # calculating similarity
            score = item_doc.similarity(cat_doc)
            
            if score > best_score:
                best_score = score
                best_category = cat
        
        # --- putting the item in the winner bucket ---
        if best_category:
            buckets[best_category].append(item_text)
            sys.stdout.write(".") # visual progress dot
            sys.stdout.flush()

    print("") # clear the line after dots
    return buckets

def main():
    # --- a little show before starting ---
    print("")
    type_writer("✨  SMART LIST ORGANIZER INITIALIZED  ✨", speed=0.05)
    type_writer("Give me a messy list, and I will sort it into categories.", speed=0.03)

    while True:
        # --- getting the input ---
        print("\nStep 1: The Messy List (Comma separated)")
        raw_items = input(">> Items: ")
        
        if raw_items.lower() in ['exit', 'quit']: 
            break
        if not raw_items.strip(): 
            continue
        
        # --- cleaning up the list (removing spaces) ---
        items = [i.strip() for i in raw_items.split(",") if i.strip()]

        print("Step 2: The Categories (Comma separated)")
        raw_cats = input(">> Categories: ")
        categories = [c.strip() for c in raw_cats.split(",") if c.strip()]

        if not categories:
            print("I need at least one category.")
            continue

        # --- running the logic ---
        sorted_buckets = organize_items(items, categories)
        
        # --- output results ---
        print("\n" + "="*30)
        type_writer("📦  ORGANIZED RESULT", speed=0.03)
        print("="*30)
        
        for category, item_list in sorted_buckets.items():
            print(f"\n📁 {category.upper()} ({len(item_list)})")
            
            if not item_list:
                print("   (Empty)")
            else:
                for item in item_list:
                    # added a little structure 
                    type_writer(f"   └─ {item}", speed=0.01)
        print("\n")

if __name__ == "__main__":
    main()



# sometimes if the categories are not too specific or fitting, it sorts words poorly