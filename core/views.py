from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Note, FlashcardDeck, Flashcard, JournalEntry, TulipVariety, ClinicalSkill, NCLEXQuestion
import json
import random

def home(request):
    return render(request, 'core/home.html')

def photobooth(request):
    return render(request, 'core/photobooth.html')

def tulips(request):
    tulip_varieties = TulipVariety.objects.all()
    if not tulip_varieties.exists():
        # Create some sample tulip data
        sample_tulips = [
            {
                'name': 'Red Emperor',
                'scientific_name': 'Tulipa fosteriana',
                'description': 'Large, brilliant red blooms that open wide in the sun. One of the earliest tulips to bloom.',
                'color': 'Bright Red',
                'bloom_time': 'Early Spring',
                'height': '12-16 inches',
                'care_instructions': 'Plant in well-drained soil in full sun to partial shade. Water regularly during growing season.',
                'image_url': 'https://images.pexels.com/photos/64241/pexels-photo-64241.jpeg'
            },
            {
                'name': 'Queen of Night',
                'scientific_name': 'Tulipa',
                'description': 'Deep purple-black blooms that are almost black in certain light. A dramatic and elegant variety.',
                'color': 'Deep Purple-Black',
                'bloom_time': 'Late Spring',
                'height': '18-24 inches',
                'care_instructions': 'Prefers full sun and well-drained, fertile soil. Allow foliage to die back naturally.',
                'image_url': 'https://images.pexels.com/photos/1166209/pexels-photo-1166209.jpeg'
            },
            {
                'name': 'White Dream',
                'scientific_name': 'Tulipa triumph',
                'description': 'Pure white petals with a subtle cream center. Perfect for creating elegant spring displays.',
                'color': 'Pure White',
                'bloom_time': 'Mid Spring',
                'height': '14-18 inches',
                'care_instructions': 'Plant bulbs 6-8 inches deep in fall. Mulch in winter for protection in cold climates.',
                'image_url': 'https://images.pexels.com/photos/1379636/pexels-photo-1379636.jpeg'
            },
            {
                'name': 'Pink Impression',
                'scientific_name': 'Tulipa darwin hybrid',
                'description': 'Large, soft pink blooms on strong stems. Excellent for cut flowers and naturalizing.',
                'color': 'Soft Pink',
                'bloom_time': 'Mid to Late Spring',
                'height': '20-24 inches',
                'care_instructions': 'Very hardy variety. Plant in full sun with good drainage. Fertilize in early spring.',
                'image_url': 'https://images.pexels.com/photos/1379637/pexels-photo-1379637.jpeg'
            },
            {
                'name': 'Yellow Crown',
                'scientific_name': 'Tulipa single early',
                'description': 'Bright yellow petals with a sunny disposition. One of the most cheerful spring bloomers.',
                'color': 'Bright Yellow',
                'bloom_time': 'Early to Mid Spring',
                'height': '12-15 inches',
                'care_instructions': 'Excellent for containers and rock gardens. Water well during growth period.',
                'image_url': 'https://images.pexels.com/photos/1379644/pexels-photo-1379644.jpeg'
            },
            {
                'name': 'Purple Prince',
                'scientific_name': 'Tulipa single late',
                'description': 'Rich purple blooms with a velvety texture. Creates stunning mass plantings.',
                'color': 'Rich Purple',
                'bloom_time': 'Late Spring',
                'height': '18-22 inches',
                'care_instructions': 'Plant in groups for best effect. Deadhead after blooming but leave foliage intact.',
                'image_url': 'https://images.pexels.com/photos/1166216/pexels-photo-1166216.jpeg'
            }
        ]
        
        for tulip_data in sample_tulips:
            TulipVariety.objects.create(**tulip_data)
        
        tulip_varieties = TulipVariety.objects.all()
    
    context = {'tulip_varieties': tulip_varieties}
    return render(request, 'core/tulips.html', context)

def games(request):
    return render(request, 'core/games.html')

def memory_game(request):
    return render(request, 'core/memory_game.html')

def quiz_game(request):
    # Mix of general nursing and tulip questions for variety
    nursing_questions = [
        {
            'question': 'What is the normal range for adult heart rate?',
            'options': ['40-60 bpm', '60-100 bpm', '100-120 bpm', '120-140 bpm'],
            'correct': 1
        },
        {
            'question': 'Which vital sign should be assessed first in an emergency?',
            'options': ['Temperature', 'Blood Pressure', 'Airway/Breathing', 'Pulse'],
            'correct': 2
        },
        {
            'question': 'What does the acronym ADPIE stand for in nursing process?',
            'options': ['Assess, Diagnose, Plan, Implement, Evaluate', 'Analyze, Develop, Perform, Inspect, Execute', 'Admit, Discharge, Plan, Intervene, Educate', 'Assess, Document, Prescribe, Inject, Examine'],
            'correct': 0
        },
        {
            'question': 'Which position is best for a patient with difficulty breathing?',
            'options': ['Supine', 'Prone', 'Fowler\'s', 'Trendelenburg'],
            'correct': 2
        },
        {
            'question': 'What is the most common route for medication administration?',
            'options': ['Intravenous', 'Intramuscular', 'Oral', 'Subcutaneous'],
            'correct': 2
        },
        {
            'question': 'What country is famous for tulip cultivation?',
            'options': ['France', 'Netherlands', 'Germany', 'Italy'],
            'correct': 1
        },
    ]
    
    # Randomly select 5 questions
    selected_questions = random.sample(nursing_questions, min(5, len(nursing_questions)))
    context = {'questions': json.dumps(selected_questions)}
    return render(request, 'core/quiz_game.html', context)

def study_companion(request):
    if request.method == 'POST':
        content = request.POST.get('journal_content', '')
        mood = request.POST.get('mood', 'neutral')
        if content:
            JournalEntry.objects.create(content=content, mood=mood)
        return JsonResponse({'success': True})
    
    recent_entries = JournalEntry.objects.order_by('-created_at')[:5]
    return render(request, 'core/study_companion.html', {'recent_entries': recent_entries})

def notes(request):
    notes = Note.objects.all().order_by('-created_at')
    subjects = Note.SUBJECT_CHOICES
    return render(request, 'core/notes.html', {'notes': notes, 'subjects': subjects})

def flashcards(request):
    decks = FlashcardDeck.objects.all()
    if not decks.exists():
        # Create nursing-focused sample decks
        fundamentals_deck = FlashcardDeck.objects.create(
            name='Nursing Fundamentals',
            description='Essential concepts every nursing student should master.'
        )
        
        fundamentals_cards = [
            {
                'question': 'What are the 5 rights of medication administration?',
                'answer': 'Right patient, Right medication, Right dose, Right route, Right time'
            },
            {
                'question': 'Define therapeutic communication',
                'answer': 'A purposeful form of communication that allows patients to express feelings and promotes healing relationships.'
            },
            {
                'question': 'What is the nursing process?',
                'answer': 'A systematic approach to patient care: Assessment, Diagnosis, Planning, Implementation, Evaluation (ADPIE)'
            },
            {
                'question': 'Normal adult blood pressure range',
                'answer': 'Systolic: 90-120 mmHg, Diastolic: 60-80 mmHg'
            }
        ]
        
        for card_data in fundamentals_cards:
            Flashcard.objects.create(deck=fundamentals_deck, **card_data)
            
        # Create pharmacology deck
        pharm_deck = FlashcardDeck.objects.create(
            name='Pharmacology Essentials',
            description='Key drug classifications and nursing considerations.'
        )
        
        pharm_cards = [
            {
                'question': 'ACE Inhibitors - Common suffix and action',
                'answer': 'Suffix: -pril (lisinopril). Action: Block conversion of angiotensin I to II, reducing blood pressure.'
            },
            {
                'question': 'Beta Blockers - Common suffix and nursing considerations',
                'answer': 'Suffix: -lol (metoprolol). Monitor heart rate and blood pressure. Do not stop abruptly.'
            },
            {
                'question': 'Diuretics - Main types and nursing considerations',
                'answer': 'Loop, thiazide, potassium-sparing. Monitor electrolytes, especially potassium. Assess for dehydration.'
            }
        ]
        
        for card_data in pharm_cards:
            Flashcard.objects.create(deck=pharm_deck, **card_data)
        
        decks = FlashcardDeck.objects.all()
    
    return render(request, 'core/flashcards.html', {'decks': decks})

def clinical_skills(request):
    skills = ClinicalSkill.objects.all()
    if not skills.exists():
        # Create sample clinical skills
        sample_skills = [
            {
                'name': 'Hand Hygiene',
                'category': 'basic',
                'description': 'Proper handwashing technique to prevent infection transmission',
                'steps': '1. Wet hands with water\n2. Apply soap\n3. Rub hands together for 20 seconds\n4. Rinse thoroughly\n5. Dry with clean towel',
                'safety_considerations': 'Use alcohol-based sanitizer when soap unavailable. Remove jewelry before washing.',
                'equipment_needed': 'Soap, running water, clean towel or paper towels',
                'competency_level': 'beginner'
            },
            {
                'name': 'Blood Pressure Measurement',
                'category': 'assessment',
                'description': 'Accurate measurement of systolic and diastolic blood pressure',
                'steps': '1. Position patient comfortably\n2. Select appropriate cuff size\n3. Place cuff 1 inch above antecubital fossa\n4. Inflate cuff 20-30 mmHg above palpated systolic\n5. Deflate slowly at 2-3 mmHg per second\n6. Record first and last Korotkoff sounds',
                'safety_considerations': 'Ensure proper cuff size. Wait 1-2 minutes between measurements.',
                'equipment_needed': 'Sphygmomanometer, stethoscope, appropriate sized cuff',
                'competency_level': 'beginner'
            },
            {
                'name': 'IV Insertion',
                'category': 'procedures',
                'description': 'Sterile insertion of intravenous catheter',
                'steps': '1. Verify order and patient identity\n2. Gather supplies\n3. Perform hand hygiene\n4. Apply tourniquet\n5. Cleanse site with antiseptic\n6. Insert catheter at 15-30 degree angle\n7. Advance catheter and remove needle\n8. Secure and document',
                'safety_considerations': 'Maintain sterile technique. Check for allergies. Monitor for infiltration.',
                'equipment_needed': 'IV catheter, antiseptic, tourniquet, tape, IV tubing, saline flush',
                'competency_level': 'intermediate'
            }
        ]
        
        for skill_data in sample_skills:
            ClinicalSkill.objects.create(**skill_data)
        
        skills = ClinicalSkill.objects.all()
    
    return render(request, 'core/clinical_skills.html', {'skills': skills})

def nclex_prep(request):
    questions = NCLEXQuestion.objects.all()
    if not questions.exists():
        # Create sample NCLEX questions
        sample_questions = [
            {
                'question_text': 'A client with heart failure is prescribed furosemide (Lasix). Which assessment finding indicates the medication is effective?',
                'question_type': 'multiple_choice',
                'options': ['Decreased urine output', 'Increased weight', 'Decreased edema', 'Increased blood pressure'],
                'correct_answers': [2],
                'rationale': 'Furosemide is a loop diuretic that removes excess fluid, reducing edema in heart failure patients.',
                'category': 'Pharmacology',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which actions should the nurse take when caring for a client with a seizure disorder? Select all that apply.',
                'question_type': 'select_all',
                'options': ['Place client in supine position', 'Insert oral airway during seizure', 'Time the duration of seizure', 'Protect client from injury', 'Administer oxygen as needed'],
                'correct_answers': [2, 3, 4],
                'rationale': 'During seizures, protect from injury, time duration, and provide oxygen if needed. Never force objects in mouth or place flat on back.',
                'category': 'Medical-Surgical',
                'difficulty': 'hard'
            }
        ]
        
        for question_data in sample_questions:
            NCLEXQuestion.objects.create(**question_data)
        
        questions = NCLEXQuestion.objects.all()
    
    # Select random questions for practice
    practice_questions = random.sample(list(questions), min(10, len(questions)))
    return render(request, 'core/nclex_prep.html', {'questions': practice_questions})