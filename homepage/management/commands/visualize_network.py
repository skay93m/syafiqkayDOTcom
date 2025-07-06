from django.core.management.base import BaseCommand
from noto_garden.models import Note, Tag
from django.db.models import Count
import json


class Command(BaseCommand):
    help = 'Export Zettelkasten network data for visualization'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['json', 'graphviz', 'summary'],
            default='summary',
            help='Output format for the network data'
        )

    def handle(self, *args, **options):
        format_type = options['format']
        
        if format_type == 'json':
            self.export_json()
        elif format_type == 'graphviz':
            self.export_graphviz()
        else:
            self.export_summary()

    def export_json(self):
        """Export network data as JSON"""
        notes = []
        connections = []
        
        for note in Note.objects.all():
            notes.append({
                'id': note.unique_id,
                'title': note.title,
                'tags': [tag.name for tag in note.tags.all()],
                'word_count': note.get_word_count(),
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            })
            
            for connected_note in note.connections.all():
                connections.append({
                    'source': note.unique_id,
                    'target': connected_note.unique_id,
                    'source_title': note.title,
                    'target_title': connected_note.title
                })
        
        network_data = {
            'notes': notes,
            'connections': connections,
            'statistics': {
                'total_notes': len(notes),
                'total_connections': len(connections),
                'total_tags': Tag.objects.count()
            }
        }
        
        self.stdout.write(json.dumps(network_data, indent=2))

    def export_graphviz(self):
        """Export network as GraphViz DOT format"""
        self.stdout.write('digraph ZettelkastenNetwork {')
        self.stdout.write('    rankdir=TB;')
        self.stdout.write('    node [shape=box, style=filled];')
        self.stdout.write('')
        
        # Add nodes
        for note in Note.objects.all():
            tag_count = note.tags.count()
            color = 'lightblue' if tag_count > 3 else 'lightgray'
            label = note.title.replace('"', '\\"')
            self.stdout.write(f'    "{note.unique_id}" [label="{label}", fillcolor={color}];')
        
        self.stdout.write('')
        
        # Add connections
        for note in Note.objects.all():
            for connected_note in note.connections.all():
                self.stdout.write(f'    "{note.unique_id}" -> "{connected_note.unique_id}";')
        
        self.stdout.write('}')

    def export_summary(self):
        """Export readable summary of the network"""
        self.stdout.write('🌸 ZETTELKASTEN NETWORK VISUALIZATION 🌸')
        self.stdout.write('='*60)
        
        # Network statistics
        total_notes = Note.objects.count()
        total_connections = sum(note.connections.count() for note in Note.objects.all())
        total_tags = Tag.objects.count()
        
        self.stdout.write(f'📊 Network Overview:')
        self.stdout.write(f'   Nodes (Notes): {total_notes}')
        self.stdout.write(f'   Edges (Connections): {total_connections}')
        self.stdout.write(f'   Labels (Tags): {total_tags}')
        self.stdout.write(f'   Density: {total_connections/(total_notes*total_notes-total_notes)*100:.1f}%')
        self.stdout.write('')
        
        # Hub analysis
        self.stdout.write('🌟 Network Hubs (Most Connected):')
        hub_analysis = []
        for note in Note.objects.all():
            in_degree = note.get_backlinks().count()
            out_degree = note.connections.count()
            total_degree = in_degree + out_degree
            hub_analysis.append((note, in_degree, out_degree, total_degree))
        
        hub_analysis.sort(key=lambda x: x[3], reverse=True)
        
        for note, in_deg, out_deg, total_deg in hub_analysis[:5]:
            self.stdout.write(f'   • {note.title[:40]:40s} ({in_deg:2d}←, {out_deg:2d}→, {total_deg:2d} total)')
        
        self.stdout.write('')
        
        # Tag clusters
        self.stdout.write('🏷️ Tag Clusters:')
        top_tags = Tag.objects.annotate(
            note_count=Count('notes')
        ).filter(note_count__gt=0).order_by('-note_count')[:8]
        
        for tag in top_tags:
            notes_with_tag = tag.notes.all()
            self.stdout.write(f'   • {tag.name:20s} ({tag.note_count:2d} notes)')
            if tag.note_count <= 3:
                for note in notes_with_tag:
                    self.stdout.write(f'     - {note.title}')
        
        self.stdout.write('')
        
        # Connection patterns
        self.stdout.write('🔗 Connection Patterns:')
        
        # Find strong bilateral connections
        bilateral_pairs = []
        for note in Note.objects.all():
            for connected in note.connections.all():
                if note in connected.connections.all():
                    pair = tuple(sorted([note.title, connected.title]))
                    if pair not in bilateral_pairs:
                        bilateral_pairs.append(pair)
        
        if bilateral_pairs:
            self.stdout.write('   Bidirectional Connections:')
            for pair in bilateral_pairs:
                self.stdout.write(f'     • {pair[0]} ↔ {pair[1]}')
        else:
            self.stdout.write('   No bidirectional connections found')
        
        self.stdout.write('')
        
        # ASCII network visualization (simplified)
        self.stdout.write('📊 Network Structure (Simplified):')
        self.stdout.write('')
        
        # Show major hubs and their connections
        for note, in_deg, out_deg, total_deg in hub_analysis[:3]:
            if total_deg > 0:
                self.stdout.write(f'   {note.title}')
                if out_deg > 0:
                    self.stdout.write(f'   ├── Connects to:')
                    for connected in note.connections.all():
                        self.stdout.write(f'   │   └── {connected.title}')
                if in_deg > 0:
                    self.stdout.write(f'   └── Connected from:')
                    for backlink in note.get_backlinks().all():
                        self.stdout.write(f'       └── {backlink.title}')
                self.stdout.write('')
        
        self.stdout.write('🎯 Recommendations:')
        self.stdout.write('   • Use hub notes as entry points for exploration')
        self.stdout.write('   • Connect isolated notes to strengthen the network')
        self.stdout.write('   • Create bridge notes between different clusters')
        self.stdout.write('   • Expand popular tag areas with new content')
        self.stdout.write('')
        self.stdout.write('🌸 Your knowledge network is ready for exploration! 🌸')
