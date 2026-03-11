import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from eduka.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = 'Seed the database with stationery products and images'

    def download_image(self, url, filename):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=15, headers=headers)
            if response.status_code == 200:
                return ContentFile(response.content, name=filename)
        except Exception as e:
            self.stdout.write(f'  Failed to download {filename}: {e}')
        return None

    def handle(self, *args, **kwargs):

        # ── STEP 1: Clear existing data ──────────────────────
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('Cleared existing data...')

        # ── STEP 2: Create categories ─────────────────────────
        pens      = Category.objects.create(name='Pens & Pencils',    slug='pens-pencils')
        notebooks = Category.objects.create(name='Notebooks & Paper', slug='notebooks-paper')
        art       = Category.objects.create(name='Art Supplies',      slug='art-supplies')
        office    = Category.objects.create(name='Office Supplies',   slug='office-supplies')
        filing    = Category.objects.create(name='Filing & Storage',  slug='filing-storage')
        adhesives = Category.objects.create(name='Adhesives & Tape',  slug='adhesives-tape')
        self.stdout.write('Created 6 categories...')

        # ── STEP 3: Products list ─────────────────────────────
        products = [

            # ── PENS & PENCILS ────────────────────────────────
            dict(
                category=pens,
                name='Bic Ballpoint Pen Blue',
                slug='bic-ballpoint-pen-blue',
                price=50, stock=500,
                image_url='https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400',
                description='A reliable everyday ballpoint pen featuring smooth blue ink that flows consistently without skipping or smearing. Ideal for students, office workers and anyone who needs a dependable writing tool. The comfortable grip ensures fatigue-free writing during long study or work sessions.',
            ),
            dict(
                category=pens,
                name='Bic Ballpoint Pen Black',
                slug='bic-ballpoint-pen-black',
                price=50, stock=500,
                image_url='https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400',
                description='Classic black ink ballpoint pen perfect for forms, signatures and everyday note-taking. Features a sturdy barrel that resists cracking and a cap that clips securely to pockets and notebooks. Trusted by students and professionals alike for consistent clean lines.',
            ),
            dict(
                category=pens,
                name='Pilot G2 Gel Pen',
                slug='pilot-g2-gel-pen',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400',
                description='The Pilot G2 is one of the most popular gel pens in the world. Its retractable fine tip delivers incredibly smooth bold lines with quick-drying gel ink that resists smearing. The contoured rubber grip provides maximum comfort during extended writing sessions.',
            ),
            dict(
                category=pens,
                name='Staedtler HB Pencil',
                slug='staedtler-hb-pencil',
                price=30, stock=800,
                image_url='https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400',
                description='A premium quality HB pencil crafted from sustainably sourced wood with a break-resistant graphite core. The HB grade offers the perfect balance between hardness and darkness making it suitable for general writing, note-taking and light sketching. Pre-sharpened and ready to use.',
            ),
            dict(
                category=pens,
                name='Faber-Castell 2B Pencil',
                slug='faber-castell-2b-pencil',
                price=40, stock=600,
                image_url='https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400',
                description='The Faber-Castell 2B pencil is a favorite among artists and students for its extra-smooth dark lines. The soft graphite core produces rich dark marks ideal for shading, sketching and artistic work. The high-quality wood casing sharpens cleanly without splintering.',
            ),
            dict(
                category=pens,
                name='Pentel Mechanical Pencil',
                slug='pentel-mechanical-pencil',
                price=299, stock=200,
                image_url='https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400',
                description='A sleek and precise mechanical pencil with a 0.5mm lead that never needs sharpening. Features a built-in eraser under the click top, a cushioned lead advance system to prevent breakage and a metal grip for accurate control. Perfect for technical drawing and detailed note-taking.',
            ),
            dict(
                category=pens,
                name='Highlighter Yellow',
                slug='highlighter-yellow',
                price=100, stock=400,
                image_url='https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400',
                description='Brighten up your notes and study materials with this vivid yellow highlighter. The chisel tip allows both broad highlighting strokes and fine underlining. The quick-drying transparent ink does not bleed through most paper types and stays bright without fading for months.',
            ),
            dict(
                category=pens,
                name='Highlighter Set 5 Colors',
                slug='highlighter-set-5-colors',
                price=450, stock=150,
                image_url='https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400',
                description='A versatile pack of five assorted highlighters in yellow, pink, green, blue and orange. Perfect for color-coded note-taking, revision and organization. Each pen features a chisel tip for both broad and narrow highlighting. The ink is water-based and safe for students of all ages.',
            ),
            dict(
                category=pens,
                name='Permanent Marker Black',
                slug='permanent-marker-black',
                price=120, stock=300,
                image_url='https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400',
                description='A bold waterproof permanent marker with quick-drying black ink that writes on almost any surface including paper, cardboard, plastic, glass and metal. The fine bullet tip produces clean consistent lines. Ideal for labeling, packaging, art projects and office use.',
            ),
            dict(
                category=pens,
                name='Whiteboard Marker Black',
                slug='whiteboard-marker-black',
                price=150, stock=250,
                image_url='https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400',
                description='A high-performance dry-erase marker designed for whiteboards, glass and other smooth surfaces. The bold black ink wipes off cleanly without leaving ghosting or residue. The low-odor formula makes it safe for classrooms and offices. Chisel tip allows both thick and thin lines.',
            ),
            dict(
                category=pens,
                name='Whiteboard Marker Set 4 Colors',
                slug='whiteboard-marker-set',
                price=499, stock=150,
                image_url='https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400',
                description='A set of four dry-erase whiteboard markers in red, blue, green and black. Each marker features a chisel tip for versatile line widths and low-odor ink safe for classroom and office use. Wipes cleanly off whiteboards without ghosting or staining.',
            ),
            dict(
                category=pens,
                name='Fountain Pen',
                slug='fountain-pen',
                price=799, stock=80,
                image_url='https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400',
                description='An elegant fountain pen with a stainless steel nib that delivers a smooth consistent ink flow for a premium writing experience. The refillable ink cartridge system is economical and environmentally friendly. Perfect for professionals, students and anyone who appreciates fine writing.',
            ),

            # ── NOTEBOOKS & PAPER ─────────────────────────────
            dict(
                category=notebooks,
                name='A4 Spiral Notebook',
                slug='a4-spiral-notebook',
                price=350, stock=300,
                image_url='https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400',
                description='A spacious A4 spiral-bound notebook with 200 pages of high-quality ruled paper. The sturdy cardboard cover protects pages from damage while the lay-flat spiral binding allows comfortable writing from edge to edge. Ideal for lectures, meetings, journaling and detailed note-taking.',
            ),
            dict(
                category=notebooks,
                name='A5 Hardcover Notebook',
                slug='a5-hardcover-notebook',
                price=599, stock=200,
                image_url='https://images.unsplash.com/photo-1544816155-12df9643f363?w=400',
                description='A sophisticated hardcover notebook with a premium cloth-textured cover and 160 pages of cream-colored lined paper. The elastic closure keeps your notes secure and the ribbon bookmark lets you find your page instantly. Small enough to carry anywhere yet spacious enough for detailed notes.',
            ),
            dict(
                category=notebooks,
                name='Exercise Book 60 Pages',
                slug='exercise-book-60-pages',
                price=80, stock=1000,
                image_url='https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400',
                description='A standard school exercise book with 60 pages of neat ruled paper and a card cover. Suitable for all subjects including maths, science and English. The wide margin allows for teacher corrections and personal annotations. Great value for schools and offices buying in bulk.',
            ),
            dict(
                category=notebooks,
                name='Exercise Book 96 Pages',
                slug='exercise-book-96-pages',
                price=120, stock=800,
                image_url='https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400',
                description='A larger exercise book with 96 pages of quality ruled paper ideal for subjects requiring extensive notes. The durable card cover withstands daily handling in school bags. The wide-ruled lines are easy to write in and the generous margins allow for marking and annotations.',
            ),
            dict(
                category=notebooks,
                name='Graph Paper Notebook',
                slug='graph-paper-notebook',
                price=250, stock=150,
                image_url='https://images.unsplash.com/photo-1544816155-12df9643f363?w=400',
                description='A specialized A4 notebook filled with 5mm grid graph paper perfect for mathematics, science diagrams, engineering sketches and data plotting. The fine grid lines are printed in light blue ink that does not interfere with your own markings. The durable cover keeps pages flat.',
            ),
            dict(
                category=notebooks,
                name='Sticky Notes Yellow',
                slug='sticky-notes-yellow',
                price=150, stock=400,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A classic yellow sticky note pad with 100 repositionable self-adhesive sheets. Perfect for reminders, to-do lists, messages and bookmarks. The strong but gentle adhesive sticks firmly to most surfaces and removes cleanly without leaving marks or residue. Each sheet is 76mm x 76mm.',
            ),
            dict(
                category=notebooks,
                name='Sticky Notes Multicolor',
                slug='sticky-notes-multicolor',
                price=299, stock=300,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A vibrant pack of five color sticky note pads in yellow, pink, green, blue and orange. Each pad contains 80 repositionable sheets for a total of 400 notes. Color coding your reminders and tasks has never been easier. Ideal for students, teachers and busy office workers.',
            ),
            dict(
                category=notebooks,
                name='A4 Printing Paper Ream',
                slug='a4-printing-paper-ream',
                price=699, stock=200,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A high-quality ream of 500 sheets of bright white A4 80gsm paper suitable for all inkjet and laser printers, photocopiers and fax machines. The smooth surface ensures sharp clear print quality with minimal ink bleed. Acid-free paper guarantees long-lasting documents.',
            ),
            dict(
                category=notebooks,
                name='Sketch Pad A4',
                slug='sketch-pad-a4',
                price=450, stock=150,
                image_url='https://images.unsplash.com/photo-1544816155-12df9643f363?w=400',
                description='A professional-quality A4 sketch pad with 50 sheets of thick 120gsm cartridge paper. The heavyweight paper handles pencil, charcoal, ink, light watercolor and mixed media without buckling or tearing. The glued binding keeps pages secure while allowing easy removal for display.',
            ),
            dict(
                category=notebooks,
                name='Ruled Loose Leaf Paper',
                slug='ruled-loose-leaf-paper',
                price=199, stock=250,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A convenient pack of 100 sheets of A4 ruled loose leaf paper with pre-punched holes for standard ring binders and lever arch files. The quality 80gsm paper is suitable for both handwriting and printing. Perfect for organizing notes by subject and adding pages to existing binders.',
            ),
            dict(
                category=notebooks,
                name='Index Cards',
                slug='index-cards',
                price=200, stock=300,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A pack of 100 blank white index cards measuring 152mm x 102mm. Ideal for flashcards, revision notes, recipe cards, presentations and filing systems. The thick card stock is durable enough for repeated handling and accepts both pen and pencil without bleeding or ghosting.',
            ),
            dict(
                category=notebooks,
                name='A4 Hardcover Notebook',
                slug='a4-hardcover-notebook',
                price=699, stock=150,
                image_url='https://images.unsplash.com/photo-1544816155-12df9643f363?w=400',
                description='A premium A4 hardcover notebook with 192 pages of thick cream ruled paper. The robust hardcover binding ensures the notebook lays flat during use and withstands daily wear and tear. An elastic band closure and inside pocket make it a complete organizational tool for professionals.',
            ),

            # ── ART SUPPLIES ──────────────────────────────────
            dict(
                category=art,
                name='Crayola Crayons 24 Pack',
                slug='crayola-crayons-24-pack',
                price=499, stock=200,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='The world-famous Crayola crayons in a classic 24-color pack including all essential shades. Made from a premium wax formula that lays down rich vibrant color with every stroke. The thick durable crayons are perfect for children and beginners while inspiring unlimited creativity.',
            ),
            dict(
                category=art,
                name='Watercolor Paint Set 12 Colors',
                slug='watercolor-paint-set',
                price=799, stock=100,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A beautifully presented 12-color watercolor paint set with a built-in mixing palette and refillable water brush. The vivid transparent pigments blend smoothly and dry to a bright clear finish. Suitable for beginners and experienced artists alike for landscapes and portraits.',
            ),
            dict(
                category=art,
                name='Colored Pencils 12 Pack',
                slug='colored-pencils-12-pack',
                price=350, stock=250,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A pack of 12 pre-sharpened colored pencils in a rainbow of assorted colors. The soft pigment-rich cores deliver smooth even color with excellent blending and layering properties. The strong wood casing sharpens cleanly and the break-resistant leads withstand everyday school use.',
            ),
            dict(
                category=art,
                name='Colored Pencils 24 Pack',
                slug='colored-pencils-24-pack',
                price=599, stock=150,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='An expanded pack of 24 richly pigmented colored pencils covering a wide spectrum of colors from vibrant primaries to subtle earth tones. The premium soft cores blend and layer beautifully for stunning artwork and detailed illustrations. Pre-sharpened in a sturdy storage tin.',
            ),
            dict(
                category=art,
                name='Acrylic Paint Set 24 Colors',
                slug='acrylic-paint-set',
                price=1299, stock=80,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A comprehensive 24-color acrylic paint set suitable for canvas, wood, paper and fabric. The fast-drying water-based formula cleans up easily while the rich pigments deliver bold opaque coverage. Ideal for beginners and intermediate artists working on school projects and fine art.',
            ),
            dict(
                category=art,
                name='Watercolor Paint Set 24 Colors',
                slug='watercolor-paint-set-24',
                price=1099, stock=80,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A professional-grade 24-color watercolor set with intensely pigmented pans that deliver stunning washes and fine detail work. The large mixing palette provides ample space for color blending. Comes in a sturdy tin case that doubles as a palette lid, perfect for painting on the go.',
            ),
            dict(
                category=art,
                name='Paint Brush Set 10 Pieces',
                slug='paint-brush-set',
                price=599, stock=150,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A versatile 10-piece paint brush set featuring a range of sizes from fine detail to broad wash brushes. The synthetic bristles are suitable for watercolor, acrylic and gouache paints. The lacquered wooden handles provide a comfortable grip and the ferrules prevent bristle shedding.',
            ),
            dict(
                category=art,
                name='Drawing Compass',
                slug='drawing-compass',
                price=399, stock=120,
                image_url='https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400',
                description='A precision metal drawing compass with a locking mechanism for consistent radius settings. The sharp steel point grips paper securely while the adjustable pencil holder accommodates standard pencils. Essential for geometry, technical drawing and creating perfect circles in art and design.',
            ),
            dict(
                category=art,
                name='Ruler 30cm',
                slug='ruler-30cm',
                price=99, stock=500,
                image_url='https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400',
                description='A clear transparent plastic ruler measuring 30cm with both metric and imperial markings. The beveled edge ensures clean straight lines without ink smearing. The anti-slip backing keeps it firmly in place during use. An essential tool for students, designers and everyday office tasks.',
            ),
            dict(
                category=art,
                name='Protractor',
                slug='protractor',
                price=80, stock=400,
                image_url='https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400',
                description='A 180-degree clear plastic protractor with easy-to-read degree markings for accurate angle measurement. The flat base ensures stable positioning on paper and the center mark allows precise alignment. An essential geometry tool for students, engineers and technical drawing work.',
            ),
            dict(
                category=art,
                name='Eraser White',
                slug='eraser-white',
                price=30, stock=1000,
                image_url='https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400',
                description='A premium soft white vinyl eraser that removes pencil marks cleanly and completely without smudging or tearing paper. The smooth texture glides effortlessly across the page leaving no colored residue behind. Suitable for all types of paper from thin tracing paper to thick cardstock.',
            ),
            dict(
                category=art,
                name='Sharpener Double Hole',
                slug='sharpener-double-hole',
                price=50, stock=800,
                image_url='https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400',
                description='A dual-hole pencil sharpener with two separate openings for standard and jumbo-sized pencils and crayons. The sharp stainless steel blades produce a clean precise point every time. The transparent barrel shows when it needs emptying and the compact size fits easily in a pencil case.',
            ),
            dict(
                category=art,
                name='Oil Pastels 12 Pack',
                slug='oil-pastels-12-pack',
                price=399, stock=120,
                image_url='https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400',
                description='A vibrant set of 12 oil pastels with rich creamy pigments that blend smoothly for stunning color effects. The soft formula allows easy layering and mixing directly on paper. Suitable for all ages and skill levels, ideal for bold illustrations, life drawing and expressive abstract artwork.',
            ),

            # ── OFFICE SUPPLIES ───────────────────────────────
            dict(
                category=office,
                name='Stapler',
                slug='stapler',
                price=499, stock=100,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A reliable desktop stapler with a full-strip capacity of 26/6 staples. The heavy-duty metal construction ensures years of dependable use in busy offices and classrooms. The easy-jam-release mechanism quickly resolves any blockages and the non-slip base keeps the stapler steady.',
            ),
            dict(
                category=office,
                name='Staples Box',
                slug='staples-box',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A box of 1000 standard 26/6 staples compatible with most desktop staplers. The galvanized steel construction ensures clean consistent stapling without jamming or bending. Each strip contains 100 staples for easy loading. An essential supply item for offices, schools and homes.',
            ),
            dict(
                category=office,
                name='Scissors',
                slug='scissors',
                price=250, stock=200,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A pair of sharp 8-inch stainless steel scissors with comfortable soft-grip handles that reduce hand fatigue during extended use. The precision-ground blades stay sharp through thousands of cuts and handle paper, card, fabric and tape with ease. Suitable for right and left-handed users.',
            ),
            dict(
                category=office,
                name='Paper Clips Box',
                slug='paper-clips-box',
                price=100, stock=400,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A box of 100 smooth silver metal paper clips in the classic Gem style. The uniform thickness and smooth finish prevent snagging and tearing of documents. Suitable for organizing loose papers, photos and documents without causing damage. An everyday essential for offices and schools.',
            ),
            dict(
                category=office,
                name='Binder Clips Small',
                slug='binder-clips-small',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A pack of 12 small black binder clips with strong spring tension that holds documents firmly without slipping. The foldback metal handles allow the clips to stand upright as a document holder or fold flat for compact storage. Ideal for keeping thin stacks of paper neatly organized.',
            ),
            dict(
                category=office,
                name='Binder Clips Large',
                slug='binder-clips-large',
                price=200, stock=200,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A pack of 12 large black binder clips capable of holding thick stacks of documents securely. The heavy-duty steel construction provides strong clamping force without damaging pages. The foldback handles can be removed for neat filing and reattached when needed.',
            ),
            dict(
                category=office,
                name='Correction Fluid',
                slug='correction-fluid',
                price=120, stock=250,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A fast-drying white correction fluid that covers mistakes cleanly and completely on most paper types. The built-in fine brush applicator allows precise application for neat corrections. The water-based formula dries in seconds and can be written over immediately without smearing.',
            ),
            dict(
                category=office,
                name='Correction Tape',
                slug='correction-tape',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A smooth-glide correction tape roller that instantly covers mistakes with clean white film. The 5mm x 8m tape dispenses evenly without tearing and can be written over immediately. The compact ergonomic dispenser fits comfortably in the hand and the refillable design is economical.',
            ),
            dict(
                category=office,
                name='Calculator',
                slug='calculator',
                price=899, stock=80,
                image_url='https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400',
                description='A versatile 12-digit desktop calculator with a large easy-to-read LCD display and responsive keys for fast accurate calculations. Features include percentage, square root, memory and tax functions. The dual power system runs on both solar and battery power for reliable use anywhere.',
            ),
            dict(
                category=office,
                name='Desk Organizer',
                slug='desk-organizer',
                price=999, stock=60,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A stylish 5-compartment desktop organizer that keeps your workspace tidy and productive. The spacious compartments accommodate pens, pencils, scissors, rulers and other essentials. Made from durable plastic with a sleek modern finish that complements any office or study space.',
            ),
            dict(
                category=office,
                name='Rubber Bands Box',
                slug='rubber-bands-box',
                price=99, stock=400,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A box of 100 premium quality rubber bands in assorted sizes suitable for bundling documents, stationery and other items. Made from natural latex for superior elasticity and durability. The bands stretch and snap back repeatedly without breaking or losing their shape.',
            ),
            dict(
                category=office,
                name='Push Pins Box',
                slug='push-pins-box',
                price=99, stock=400,
                image_url='https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=400',
                description='A box of 100 colorful push pins with sharp steel points that penetrate noticeboards and cork boards with minimal effort. The smooth rounded plastic heads are easy to grip and remove. Available in assorted bright colors for color-coded organization of schedules, maps and notices.',
            ),

            # ── FILING & STORAGE ──────────────────────────────
            dict(
                category=filing,
                name='A4 Ring Binder',
                slug='a4-ring-binder',
                price=399, stock=150,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A sturdy A4 two-ring binder with a clear overlay cover for custom labeling. The smooth-action rings open and close securely without snagging pages and the durable PVC cover resists wear and moisture. Ideal for organizing school notes, work documents and reference materials.',
            ),
            dict(
                category=filing,
                name='Document Folder',
                slug='document-folder',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A clear A4 plastic document folder with a secure press-stud fastener that keeps contents safe and neatly organized. The transparent cover allows quick identification of contents without opening the folder. Lightweight and slim enough to carry multiple folders in a bag.',
            ),
            dict(
                category=filing,
                name='Lever Arch File',
                slug='lever-arch-file',
                price=450, stock=100,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A robust A4 lever arch file with a 70mm spine capacity holding up to 500 sheets. The smooth metal lever mechanism opens and closes with one hand for easy access. The spine label holder allows clear identification and the durable board construction withstands heavy daily use.',
            ),
            dict(
                category=filing,
                name='Manila Envelope A4',
                slug='manila-envelope-a4',
                price=50, stock=500,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A strong brown manila envelope in A4 size with a secure self-seal adhesive strip for quick closure. The tough kraft paper construction protects documents during mailing and storage. Suitable for letters, certificates, reports and official correspondence.',
            ),
            dict(
                category=filing,
                name='Plastic Wallet A4',
                slug='plastic-wallet-a4',
                price=40, stock=600,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A clear A4 plastic document wallet with an open top for quick insertion and removal of papers. The durable polypropylene material is waterproof and tear-resistant, protecting important documents from spills and moisture. Fits standard ring binders and lever arch files.',
            ),
            dict(
                category=filing,
                name='Filing Box',
                slug='filing-box',
                price=799, stock=50,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A heavy-duty cardboard filing box designed to store and transport A4 documents, files and folders. The secure lid keeps contents dust-free during long-term storage. The built-in handles make it easy to carry and the stackable design saves space in offices and storerooms.',
            ),
            dict(
                category=filing,
                name='Presentation Folder',
                slug='presentation-folder',
                price=250, stock=200,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A professional A4 presentation folder with twin pockets for holding loose documents, business cards and brochures. The glossy cover gives a polished impression in meetings. Suitable for proposals, reports, portfolios and any situation where a professional appearance matters.',
            ),
            dict(
                category=filing,
                name='Expanding File 13 Sections',
                slug='expanding-file',
                price=599, stock=80,
                image_url='https://images.unsplash.com/photo-1568667256549-094345857637?w=400',
                description='A portable A4 expanding file with 13 tabbed sections for comprehensive document organization. The secure elastic closure keeps all contents safely inside and the lightweight plastic construction makes it easy to carry. Color-coded tabs allow instant identification for fast filing.',
            ),

            # ── ADHESIVES & TAPE ──────────────────────────────
            dict(
                category=adhesives,
                name='Sellotape Clear',
                slug='sellotape-clear',
                price=100, stock=400,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A versatile roll of 19mm x 33m clear adhesive tape that is an absolute essential for any desk, office or home. The strong transparent adhesive bonds instantly to paper, card and most smooth surfaces. The tape tears cleanly by hand and the finish is nearly invisible once applied.',
            ),
            dict(
                category=adhesives,
                name='Masking Tape',
                slug='masking-tape',
                price=150, stock=300,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A 24mm x 50m roll of high-quality masking tape with a gentle adhesive that sticks firmly yet removes cleanly without leaving residue or damaging surfaces. Ideal for painting, crafts, labeling and general repairs. The easy-tear paper backing allows precise application.',
            ),
            dict(
                category=adhesives,
                name='Pritt Stick Glue',
                slug='pritt-stick-glue',
                price=120, stock=350,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='The original Pritt Stick glue in a 20g twist-up format that is clean, safe and easy to use for all ages. The smooth formula spreads evenly without lumps and bonds paper, card and photos instantly. Non-toxic and solvent-free, perfect for school projects and craft activities.',
            ),
            dict(
                category=adhesives,
                name='UHU All Purpose Glue',
                slug='uhu-all-purpose-glue',
                price=250, stock=200,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A powerful 35ml tube of UHU all-purpose adhesive that bonds paper, card, fabric, leather, wood, ceramics and most plastics. The strong flexible bond withstands stress after drying. The precision nozzle allows controlled application for both large surfaces and fine detail work.',
            ),
            dict(
                category=adhesives,
                name='Double Sided Tape',
                slug='double-sided-tape',
                price=199, stock=250,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A 12mm x 10m roll of double-sided adhesive tape that creates invisible bonds between paper, card, photos and fabric. The strong permanent adhesive holds firmly without wrinkling. Ideal for scrapbooking, card making, mounting photos and any craft project requiring invisible tape.',
            ),
            dict(
                category=adhesives,
                name='Glue Gun',
                slug='glue-gun',
                price=899, stock=60,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A versatile electric hot glue gun that melts standard glue sticks for fast strong bonding of paper, card, wood, fabric and plastic. The ergonomic trigger provides precise control over glue flow and the insulated nozzle prevents accidental burns. Includes 5 glue sticks to get started.',
            ),
            dict(
                category=adhesives,
                name='Glue Sticks Refill Pack',
                slug='glue-sticks-refill-pack',
                price=299, stock=150,
                image_url='https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400',
                description='A pack of 20 standard hot glue sticks compatible with most electric glue guns. The high-strength formula melts quickly and bonds firmly to wood, fabric, paper, plastic and ceramics. Each stick measures 11mm in diameter and 10cm in length for long-lasting economical use.',
            ),
        ]

        # ── STEP 4: Create products and download images ───────
        success_count = 0
        for p in products:
            image_url = p.pop('image_url', None)
            product = Product.objects.create(**p, available=True)

            if image_url:
                image_file = self.download_image(image_url, f"{product.slug}.jpg")
                if image_file:
                    ProductImage.objects.create(
                        product=product,
                        image=image_file,
                        alt=product.name,
                        is_main=True
                    )
                    self.stdout.write(f'  ✅ {product.name}')
                    success_count += 1
                else:
                    self.stdout.write(f'  ⚠️  {product.name} — no image')
            else:
                self.stdout.write(f'  ➕ {product.name} — created without image')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(products)} products created, {success_count} with images across 6 categories.'
        ))