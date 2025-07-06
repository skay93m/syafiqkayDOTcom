from django.core.management.base import BaseCommand
from noto_garden.models import Note, Tag
from django.db.models import Count
import json


class Command(BaseCommand):
    help = 'Demonstrate the Zettelkasten network structure and connections'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🌸 ZETTELKASTEN NETWORK DEMONSTRATION 🌸')
        )
        self.stdout.write('=' * 60)
        
        # Basic statistics
        total_notes = Note.objects.count()
        total_tags = Tag.objects.count()
        total_connections = sum(note.connections.count() for note in Note.objects.all())
        
        self.stdout.write(f'📊 Network Statistics:')
        self.stdout.write(f'   • Total Notes: {total_notes}')
        self.stdout.write(f'   • Total Tags: {total_tags}')
        self.stdout.write(f'   • Total Connections: {total_connections}')
        self.stdout.write(f'   • Average Connections per Note: {total_connections/total_notes:.1f}')
        self.stdout.write()
        
        # Show network structure
        self.stdout.write('🔗 Network Structure:')
        self.stdout.write('-' * 40)
        
        for note in Note.objects.all().order_by('title'):
            connections = note.connections.all()
            backlinks = note.get_backlinks()
            tags = note.tags.all()
            
            self.stdout.write(f'\\n📝 {note.title}')
            self.stdout.write(f'   ID: {note.unique_id}')
            self.stdout.write(f'   Tags: {", ".join([tag.name for tag in tags])}')
            self.stdout.write(f'   Word Count: {note.get_word_count()}')
            
            if connections:
                self.stdout.write(f'   → Outgoing Connections ({connections.count()}):')
                for conn in connections:
                    self.stdout.write(f'     • {conn.title} ({conn.unique_id})')
                    
            if backlinks:
                self.stdout.write(f'   ← Incoming Connections ({backlinks.count()}):')
                for back in backlinks:
                    self.stdout.write(f'     • {back.title} ({back.unique_id})')
            
            if not connections and not backlinks:
                self.stdout.write(f'   ⚠️  No connections (consider linking!)')
        
        self.stdout.write()
        self.stdout.write('🏷️ Tag Cloud Analysis:')
        self.stdout.write('-' * 40)
        
        # Most used tags
        top_tags = Tag.objects.annotate(
            note_count=Count('notes')
        ).filter(note_count__gt=0).order_by('-note_count')[:10]
        
        for tag in top_tags:
            self.stdout.write(f'   • {tag.name}: {tag.note_count} notes')
        
        self.stdout.write()
        self.stdout.write('🌟 Knowledge Clusters:')
        self.stdout.write('-' * 40)
        
        # Find highly connected notes (knowledge hubs)
        hub_notes = []
        for note in Note.objects.all():
            total_connections = note.connections.count() + note.get_backlinks().count()
            if total_connections >= 3:
                hub_notes.append((note, total_connections))
        
        hub_notes.sort(key=lambda x: x[1], reverse=True)
        
        for note, connection_count in hub_notes:
            self.stdout.write(f'   🌟 {note.title}: {connection_count} connections')
            
        self.stdout.write()
        self.stdout.write('📍 Potential Growth Areas:')
        self.stdout.write('-' * 40)
        
        # Find notes with few connections
        isolated_notes = []
        for note in Note.objects.all():
            total_connections = note.connections.count() + note.get_backlinks().count()
            if total_connections <= 1:
                isolated_notes.append(note)
        
        for note in isolated_notes:
            self.stdout.write(f'   • {note.title} - Consider adding connections')
        
        self.stdout.write()
        self.stdout.write('🎯 Zettelkasten Recommendations:')
        self.stdout.write('-' * 40)
        self.stdout.write('   1. Connect isolated notes to build knowledge clusters')
        self.stdout.write('   2. Expand on high-value tags with new notes')
        self.stdout.write('   3. Create bridge notes between different concept areas')
        self.stdout.write('   4. Use hub notes as starting points for exploration')
        self.stdout.write('   5. Review and refine tag taxonomy regularly')
        
        self.stdout.write()
        self.stdout.write('🎉 Your Zettelkasten demonstrates:')
        self.stdout.write('   ✅ Interconnected knowledge network')
        self.stdout.write('   ✅ Emergent concept clusters')
        self.stdout.write('   ✅ Multiple pathways for discovery')
        self.stdout.write('   ✅ Scalable knowledge architecture')
        self.stdout.write()
        self.stdout.write('🌸 Happy knowledge gardening! 🌸')
