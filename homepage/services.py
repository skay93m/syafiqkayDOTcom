'''
<!-- Personal Statement Section -->
{% if rirekisho %}
    <div class="row mb-5">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h4 class="card-title mb-0">🥷 Personal Statement</h4>
                </div>
                <div class="card-body">
                    <div class="card-text">{{ rirekisho.personal_statement|markdown }}
                </div>
                <div class="text-muted"><small>📅 Created: {{ rirekisho.created_at|date:"M d, Y H:i" }}</small>
                </div>
            </div>
        </div>
    </div>
{% else %}
<div class="row mb-5">
    <div class="col-md-12">
        <div class="card border">
            <div class="card-body text-center">
                <h4 class="card-title">🥷 Welcome to the Digital Dojo</h4>
                <p class="card-text">No Rirekisho data available. Please check back later.</p>
            </div>
        </div>
    </div>
</div>
'''