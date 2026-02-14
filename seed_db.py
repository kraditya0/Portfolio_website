"""
Seed the database with sample data for the portfolio website.
Run this once: python seed_db.py
"""
import os
import sys

# Ensure we can import models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    init_db, add_project, add_service, add_skill, add_testimonial,
    get_all_projects, get_all_services, get_all_skills, get_approved_testimonials
)

def seed():
    """Seed the database with sample data if tables are empty."""

    # ─── Seed Services ──────────────────────────────────────
    if not get_all_services():
        print("Seeding services...")
        services = [
            ("Flask Web Application Development",
             "Custom web applications built with Flask, featuring authentication, database integration, REST APIs, and modern responsive UI.",
             "bi-globe", "$500 - $3000"),

            ("AI Chatbot Integration",
             "Intelligent chatbot solutions powered by AI/ML, integrated into your website or application for 24/7 customer support.",
             "bi-robot", "$800 - $4000"),

            ("REST API Development",
             "Scalable and secure RESTful APIs with proper authentication, documentation, rate limiting, and comprehensive testing.",
             "bi-hdd-network", "$400 - $2500"),

            ("Database Design & Optimization",
             "Efficient database architecture design, query optimization, migration scripts, and data modeling for any scale.",
             "bi-database", "$300 - $1500"),

            ("E-commerce Website Development",
             "Full-featured online stores with payment integration, inventory management, user accounts, and admin dashboard.",
             "bi-cart4", "$1500 - $5000"),

            ("Automation & Scripting",
             "Python automation scripts for data processing, web scraping, report generation, and workflow optimization.",
             "bi-gear-wide-connected", "$200 - $1500"),
        ]
        for title, desc, icon, price in services:
            add_service(title, desc, icon, price)
        print(f"  Added {len(services)} services.")

    # ─── Seed Projects ──────────────────────────────────────
    if not get_all_projects():
        print("Seeding projects...")
        projects = [
            ("Vehicle Parking Management System",
             "A smart parking management application with real-time slot availability tracking, automated billing, vehicle entry/exit logging, and an intuitive dashboard for parking lot operators.",
             "",
             "", "", ""),

            ("Hospital Management System",
             "Comprehensive hospital management platform with patient registration, appointment scheduling, doctor management, medical records, billing, and pharmacy inventory tracking.",
             "",
             "", "", ""),

            ("Placement Portal",
             "An end-to-end campus placement platform with student profiles, company job postings, application tracking, interview scheduling, and placement statistics dashboard.",
             "",
             "", "", ""),
        ]
        for title, desc, tech, github, live, img in projects:
            add_project(title, desc, tech, github, live, img)
        print(f"  Added {len(projects)} projects.")

    # ─── Seed Skills ────────────────────────────────────────
    if not get_all_skills():
        print("Seeding skills...")
        skills = [
            ("Python", 92, "Backend"),
            ("Flask", 88, "Backend"),
            ("JavaScript", 82, "Frontend"),
            ("Vue.js", 78, "Frontend"),
            ("SQL & Database Design", 87, "Backend"),
            ("Bootstrap & CSS", 85, "Frontend"),
            ("REST API Design", 90, "Backend"),
            ("Git & Version Control", 88, "Tools"),
            ("AI / Machine Learning", 75, "Technical"),
        ]
        for name, pct, cat in skills:
            add_skill(name, pct, cat)
        print(f"  Added {len(skills)} skills.")

    # ─── Seed Testimonials ──────────────────────────────────
    if not get_approved_testimonials():
        print("Seeding testimonials...")
        testimonials = [
            ("Rahul Sharma", "Startup Founder", 5,
             "Aditya built our complete web platform from scratch. His Flask expertise and clean code practices made the project a success. Highly recommended!"),
            ("Priya Patel", "Business Owner", 5,
             "Outstanding work on our e-commerce website. The payment integration and admin dashboard were exactly what we needed. Very professional!"),
            ("Amit Verma", "Project Manager", 4,
             "Great communication throughout the project. Delivered the REST API ahead of schedule with comprehensive documentation. Will hire again!"),
        ]
        for name, role, rating, feedback in testimonials:
            add_testimonial(name, role, rating, feedback)
        print(f"  Added {len(testimonials)} testimonials.")

    print("\nDatabase seeded successfully!")
    print("You can now run: python app.py")

if __name__ == '__main__':
    seed()
